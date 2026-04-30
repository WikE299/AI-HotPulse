import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import settings

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def _crawl_job():
    from app.pipeline import run_crawl_pipeline
    try:
        count = await run_crawl_pipeline()
        logger.info("Crawl completed: %d new articles", count)
    except Exception as e:
        logger.error("Crawl failed: %s", e)


async def _brief_job():
    from app.database import AsyncSessionLocal
    from app.models.article import Article
    from app.models.brief import DailyBrief
    from app.analysis.brief_generator import generate_daily_brief
    from datetime import datetime, timezone
    from sqlalchemy import select, desc
    import json, uuid

    try:
        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        async with AsyncSessionLocal() as db:
            existing = (await db.scalars(
                select(DailyBrief).where(DailyBrief.date == today)
            )).first()
            if existing:
                return

            articles = (await db.scalars(
                select(Article)
                .order_by(desc(Article.heat_score), desc(Article.published_at))
                .limit(20)
            )).all()

            if not articles:
                return

            content = await generate_daily_brief(today, list(articles))
            brief = DailyBrief(
                id=str(uuid.uuid4()),
                date=today,
                content=content,
                article_ids=json.dumps([a.id for a in articles]),
                generated_at=datetime.now(tz=timezone.utc),
            )
            db.add(brief)
            await db.commit()
        logger.info("Daily brief generated for %s", today)
    except Exception as e:
        logger.error("Brief generation failed: %s", e)


def start_scheduler():
    scheduler.add_job(
        _crawl_job,
        "cron",
        hour=settings.crawl_schedule_hour,
        minute=settings.crawl_schedule_minute,
        id="daily_crawl",
        replace_existing=True,
    )
    scheduler.add_job(
        _brief_job,
        "cron",
        hour=9,
        minute=5,
        id="daily_brief",
        replace_existing=True,
    )
    scheduler.start()


def shutdown_scheduler():
    scheduler.shutdown(wait=False)
