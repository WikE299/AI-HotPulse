from datetime import datetime, timezone

import feedparser
import httpx
from bs4 import BeautifulSoup

from app.crawlers.base import BaseCrawler, RawArticle

RSS_SOURCES = [
    # 中文
    ("机器之心", "chinese", "https://www.jiqizhixin.com/rss"),
    ("量子位", "chinese", "https://www.qbitai.com/feed"),
    ("36kr AI", "chinese", "https://36kr.com/feed"),
    # 英文
    ("TechCrunch AI", "english", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("The Verge AI", "english", "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml"),
    ("MIT Tech Review", "english", "https://www.technologyreview.com/feed/"),
]


def _parse_time(entry) -> datetime | None:
    t = entry.get("published_parsed") or entry.get("updated_parsed")
    if t:
        return datetime(*t[:6], tzinfo=timezone.utc)
    return None


def _extract_image(entry) -> str | None:
    if hasattr(entry, "media_content") and entry.media_content:
        return entry.media_content[0].get("url")
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        return entry.media_thumbnail[0].get("url")
    content = entry.get("summary", "")
    soup = BeautifulSoup(content, "lxml")
    img = soup.find("img")
    return img["src"] if img and img.get("src") else None


def _extract_snippet(entry) -> str | None:
    raw = entry.get("summary") or entry.get("content", [{}])[0].get("value", "")
    text = BeautifulSoup(raw, "lxml").get_text(" ", strip=True)
    return text[:500] if text else None


class RSSCrawler(BaseCrawler):
    async def fetch(self) -> list[RawArticle]:
        articles: list[RawArticle] = []
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            for source_name, source_type, url in RSS_SOURCES:
                try:
                    resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0 AI-HotPulse/1.0"})
                    feed = feedparser.parse(resp.text)
                    for entry in feed.entries[:20]:
                        link = entry.get("link", "")
                        title = entry.get("title", "").strip()
                        if not link or not title:
                            continue
                        articles.append(
                            RawArticle(
                                title=title,
                                original_url=link,
                                source=source_name,
                                source_type=source_type,
                                published_at=_parse_time(entry),
                                image_url=_extract_image(entry),
                                content_snippet=_extract_snippet(entry),
                            )
                        )
                except Exception:
                    pass
        return articles
