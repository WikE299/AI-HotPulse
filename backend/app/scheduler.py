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


def start_scheduler():
    scheduler.add_job(
        _crawl_job,
        "cron",
        hour=settings.crawl_schedule_hour,
        minute=settings.crawl_schedule_minute,
        id="daily_crawl",
        replace_existing=True,
    )
    scheduler.start()


def shutdown_scheduler():
    scheduler.shutdown(wait=False)
