from datetime import datetime, timezone

import httpx

from app.crawlers.base import BaseCrawler, RawArticle

HN_TOP_STORIES = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"
AI_KEYWORDS = {"ai", "gpt", "llm", "ml", "machine learning", "deep learning", "neural",
               "openai", "anthropic", "gemini", "claude", "diffusion", "transformer"}


class HackerNewsCrawler(BaseCrawler):
    async def fetch(self) -> list[RawArticle]:
        articles: list[RawArticle] = []
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(HN_TOP_STORIES)
            story_ids = resp.json()[:100]

            import asyncio
            semaphore = asyncio.Semaphore(10)

            async def fetch_item(item_id: int) -> RawArticle | None:
                async with semaphore:
                    try:
                        r = await client.get(HN_ITEM.format(item_id))
                        item = r.json()
                        if item.get("type") != "story" or not item.get("url"):
                            return None
                        title = (item.get("title") or "").lower()
                        if not any(kw in title for kw in AI_KEYWORDS):
                            return None
                        return RawArticle(
                            title=item["title"],
                            original_url=item["url"],
                            source="HackerNews",
                            source_type="english",
                            published_at=datetime.fromtimestamp(item["time"], tz=timezone.utc) if item.get("time") else None,
                            content_snippet=f"Score: {item.get('score', 0)} | Comments: {item.get('descendants', 0)}",
                        )
                    except Exception:
                        return None

            results = await asyncio.gather(*[fetch_item(i) for i in story_ids])
            articles = [r for r in results if r is not None]
        return articles
