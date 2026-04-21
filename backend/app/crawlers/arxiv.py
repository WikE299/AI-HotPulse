from datetime import datetime, timezone

import feedparser
import httpx

from app.crawlers.base import BaseCrawler, RawArticle

ARXIV_FEED = (
    "https://export.arxiv.org/api/query"
    "?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL"
    "&sortBy=submittedDate&sortOrder=descending&max_results=30"
)


class ArXivCrawler(BaseCrawler):
    async def fetch(self) -> list[RawArticle]:
        articles: list[RawArticle] = []
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                resp = await client.get(ARXIV_FEED)
                feed = feedparser.parse(resp.text)
                for entry in feed.entries:
                    link = entry.get("link", "")
                    title = entry.get("title", "").replace("\n", " ").strip()
                    summary = entry.get("summary", "").replace("\n", " ").strip()
                    published_str = entry.get("published", "")
                    published_at = None
                    if published_str:
                        try:
                            published_at = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
                        except ValueError:
                            pass
                    if not link or not title:
                        continue
                    articles.append(
                        RawArticle(
                            title=title,
                            original_url=link,
                            source="ArXiv",
                            source_type="academic",
                            published_at=published_at,
                            content_snippet=summary[:500] if summary else None,
                        )
                    )
            except Exception:
                pass
        return articles
