import asyncio

from app.analysis.brief_generator import generate_daily_brief
from app.database import AsyncSessionLocal, init_db
from app.models.article import Article
from app.models.brief import DailyBrief
from app.pipeline import run_crawl_pipeline
from datetime import datetime, timezone
from sqlalchemy import desc, select
import json
import uuid


async def ensure_daily_brief() -> None:
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


async def main() -> None:
    await init_db()
    count = await run_crawl_pipeline()
    await ensure_daily_brief()
    print(f"Crawl completed, {count} articles added")


if __name__ == "__main__":
    asyncio.run(main())
