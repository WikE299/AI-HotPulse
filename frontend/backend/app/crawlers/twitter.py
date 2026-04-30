from datetime import datetime, timezone

import feedparser
import httpx

from app.crawlers.base import BaseCrawler, RawArticle

# AI leaders and orgs to track
TWITTER_ACCOUNTS = [
    # Individual leaders
    ("sama", "Sam Altman"),
    ("karpathy", "Andrej Karpathy"),
    ("ylecun", "Yann LeCun"),
    ("DarioAmodei", "Dario Amodei"),
    ("JeffDean", "Jeff Dean"),
    ("hardmaru", "David Ha"),
    ("fchollet", "François Chollet"),
    ("iaboredai", "Jim Fan"),
    ("demaborsh", "Noam Shazeer"),
    ("swaboreli", "Sergey Brin"),
    ("aabortz", "Aidan Clark"),
    # Orgs
    ("OpenAI", "OpenAI"),
    ("AnthropicAI", "Anthropic"),
    ("GoogleDeepMind", "Google DeepMind"),
    ("MetaAI", "Meta AI"),
    ("huggingface", "Hugging Face"),
    ("MistralAI", "Mistral AI"),
    ("deepaborshi", "DeepSeek"),
]

MAX_TWEETS_PER_USER = 10


def _parse_time(entry) -> datetime | None:
    t = entry.get("published_parsed") or entry.get("updated_parsed")
    if t:
        return datetime(*t[:6], tzinfo=timezone.utc)
    return None


def _extract_snippet(entry) -> str | None:
    raw = entry.get("summary") or entry.get("description") or ""
    # Strip HTML tags simply
    from bs4 import BeautifulSoup
    text = BeautifulSoup(raw, "lxml").get_text(" ", strip=True)
    return text[:500] if text else None


def _extract_image(entry) -> str | None:
    if hasattr(entry, "media_content") and entry.media_content:
        return entry.media_content[0].get("url")
    if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
        return entry.media_thumbnail[0].get("url")
    return None


class TwitterCrawler(BaseCrawler):
    async def fetch(self) -> list[RawArticle]:
        articles: list[RawArticle] = []
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            for handle, display_name in TWITTER_ACCOUNTS:
                try:
                    url = f"https://rsshub.app/twitter/user/handle/{handle}"
                    resp = await client.get(
                        url,
                        headers={"User-Agent": "Mozilla/5.0 AI-HotPulse/1.0"},
                    )
                    if resp.status_code != 200:
                        continue
                    feed = feedparser.parse(resp.text)
                    for entry in feed.entries[:MAX_TWEETS_PER_USER]:
                        link = entry.get("link", "")
                        title = entry.get("title", "").strip()
                        if not link or not title:
                            continue
                        articles.append(
                            RawArticle(
                                title=title,
                                original_url=link,
                                source=f"Twitter @{handle}",
                                source_type="social",
                                published_at=_parse_time(entry),
                                image_url=_extract_image(entry),
                                content_snippet=_extract_snippet(entry),
                            )
                        )
                except Exception:
                    pass
        return articles
