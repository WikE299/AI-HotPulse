from datetime import datetime, timezone
import uuid

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.analysis.claude_analyzer import analyze_batch
from app.crawlers.arxiv import ArXivCrawler
from app.crawlers.hackernews import HackerNewsCrawler
from app.crawlers.reddit import RedditCrawler
from app.crawlers.rss_crawler import RSSCrawler
from app.database import AsyncSessionLocal
from app.models.article import Article


async def run_crawl_pipeline():
    crawlers = [RSSCrawler(), HackerNewsCrawler(), ArXivCrawler(), RedditCrawler()]
    all_raw = []
    for crawler in crawlers:
        try:
            results = await crawler.fetch()
            all_raw.extend(results)
        except Exception:
            pass

    async with AsyncSessionLocal() as db:
        # Filter already-known URLs
        urls = [a.original_url for a in all_raw]
        existing = await db.scalars(select(Article.original_url).where(Article.original_url.in_(urls)))
        existing_urls = set(existing.all())
        new_articles = [a for a in all_raw if a.original_url not in existing_urls]

        if not new_articles:
            return 0

        analyses = await analyze_batch(new_articles)

        for raw, analysis in zip(new_articles, analyses):
            article = Article(
                title=raw.title,
                source=raw.source,
                source_type=raw.source_type,
                original_url=raw.original_url,
                published_at=raw.published_at,
                crawled_at=datetime.now(tz=timezone.utc),
                image_url=raw.image_url,
                content_snippet=raw.content_snippet,
                summary=analysis.get("summary"),
                keywords=analysis.get("keywords") or [],
                category=analysis.get("category", "Other"),
                heat_score=analysis.get("heat_score", 0),
            )
            db.add(article)

        await db.commit()
    return len(new_articles)
