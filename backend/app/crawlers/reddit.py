from datetime import datetime, timezone

import httpx

from app.crawlers.base import BaseCrawler, RawArticle

REDDIT_URL = "https://www.reddit.com/r/MachineLearning/hot.json?limit=25"
HEADERS = {"User-Agent": "AI-HotPulse/1.0 (educational project)"}


class RedditCrawler(BaseCrawler):
    async def fetch(self) -> list[RawArticle]:
        articles: list[RawArticle] = []
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            try:
                resp = await client.get(REDDIT_URL, headers=HEADERS)
                data = resp.json()
                posts = data.get("data", {}).get("children", [])
                for post in posts:
                    p = post.get("data", {})
                    url = p.get("url", "")
                    title = p.get("title", "").strip()
                    if not url or not title or url.startswith("https://www.reddit.com"):
                        continue
                    created = p.get("created_utc")
                    published_at = datetime.fromtimestamp(created, tz=timezone.utc) if created else None
                    thumbnail = p.get("thumbnail", "")
                    image_url = thumbnail if thumbnail.startswith("http") else None
                    snippet = p.get("selftext", "")[:500] or f"Upvotes: {p.get('score', 0)}"
                    articles.append(
                        RawArticle(
                            title=title,
                            original_url=url,
                            source="Reddit r/MachineLearning",
                            source_type="social",
                            published_at=published_at,
                            image_url=image_url,
                            content_snippet=snippet,
                        )
                    )
            except Exception:
                pass
        return articles
