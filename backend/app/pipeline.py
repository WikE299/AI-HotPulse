from datetime import datetime, timezone
import json

from sqlalchemy import text

from app.config import settings
from app.crawlers.arxiv import ArXivCrawler
from app.crawlers.hackernews import HackerNewsCrawler
from app.crawlers.reddit import RedditCrawler
from app.crawlers.rss_crawler import RSSCrawler
from app.database import AsyncSessionLocal


async def run_crawl_pipeline():
    crawlers = [RSSCrawler(), HackerNewsCrawler(), ArXivCrawler(), RedditCrawler()]
    all_raw = []
    for crawler in crawlers:
        try:
            results = await crawler.fetch()
            all_raw.extend(results)
        except Exception:
            pass

    # Deduplicate within batch
    seen: set[str] = set()
    unique_raw = []
    for a in all_raw:
        if a.original_url not in seen:
            seen.add(a.original_url)
            unique_raw.append(a)

    if not unique_raw:
        return 0

    # Run AI analysis only when API key is configured
    if settings.anthropic_api_key:
        from app.analysis.claude_analyzer import analyze_batch
        analyses = await analyze_batch(unique_raw)
    else:
        analyses = [{"summary": None, "keywords": [], "category": "Other", "heat_score": 0}] * len(unique_raw)

    import uuid
    now = datetime.now(tz=timezone.utc).isoformat()
    rows = []
    for raw, analysis in zip(unique_raw, analyses):
        rows.append({
            "id": str(uuid.uuid4()),
            "title": raw.title,
            "source": raw.source,
            "source_type": raw.source_type,
            "original_url": raw.original_url,
            "published_at": raw.published_at.isoformat() if raw.published_at else None,
            "crawled_at": now,
            "image_url": raw.image_url,
            "content_snippet": raw.content_snippet,
            "summary": analysis.get("summary"),
            "keywords": json.dumps(analysis.get("keywords") or []),
            "category": analysis.get("category", "Other"),
            "heat_score": analysis.get("heat_score", 0),
        })

    async with AsyncSessionLocal() as db:
        for row in rows:
            await db.execute(
                text(
                    "INSERT OR IGNORE INTO articles "
                    "(id, title, source, source_type, original_url, published_at, crawled_at, "
                    "image_url, content_snippet, summary, keywords, category, heat_score) "
                    "VALUES (:id, :title, :source, :source_type, :original_url, :published_at, :crawled_at, "
                    ":image_url, :content_snippet, :summary, :keywords, :category, :heat_score)"
                ),
                row,
            )
        await db.commit()

    return len(rows)
