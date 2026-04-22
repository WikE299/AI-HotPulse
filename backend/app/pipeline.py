from datetime import datetime, timezone, timedelta
import json
import re
import uuid

from sqlalchemy import text

from app.config import settings
from app.crawlers.arxiv import ArXivCrawler
from app.crawlers.hackernews import HackerNewsCrawler
from app.crawlers.reddit import RedditCrawler
from app.crawlers.rss_crawler import RSSCrawler
from app.database import AsyncSessionLocal

_AI_KEYWORDS = re.compile(
    r"ai\b|a\.i\.|人工智能|artificial intelligence"
    r"|machine learning|deep learning|机器学习|深度学习"
    r"|neural|神经网络|transformer|diffusion"
    r"|llm|large language|大语言模型|大模型"
    r"|gpt|claude|gemini|mistral|llama|qwen|deepseek|kimi|moonshot"
    r"|openai|anthropic|google deepmind|hugging.?face|meta ai"
    r"|agent|智能体|多智能体|agentic|autonomous"
    r"|rag|retrieval.augmented|向量检索|向量数据库"
    r"|fine.?tun|微调|预训练|pretrain"
    r"|computer vision|cv\b|目标检测|图像识别|图像生成"
    r"|nlp|自然语言|text.to|文生图|文生视频"
    r"|robotics|机器人|具身智能|embodied"
    r"|stable diffusion|midjourney|sora|runway"
    r"|prompt|inference|推理|量化|模型压缩"
    r"|benchmark|leaderboard|排行榜|评测",
    re.IGNORECASE,
)

_TOPIC_PATTERNS = [
    (r"gpt-?5|gpt5", "openai-gpt5"),
    (r"gpt-?4[^0-9]|gpt4[^0-9]|gpt-?4o", "openai-gpt4"),
    (r"claude\s*[34]", "anthropic-claude"),
    (r"gemini\s*\d+|gemini ultra|gemini pro|gemini flash", "google-gemini"),
    (r"llama\s*[34]", "meta-llama"),
    (r"\bdeepseek\b", "deepseek"),
    (r"\bsora\b", "openai-sora"),
    (r"\bopenai\b", "openai"),
    (r"\banthropic\b", "anthropic"),
    (r"google\s+ai|google deepmind", "google-ai"),
    (r"\bmistral\b", "mistral"),
    (r"\bkimi\b|\bmoonshot\b", "moonshot-kimi"),
]


def _is_ai_related(title: str, snippet: str | None) -> bool:
    text_str = (title or "") + " " + (snippet or "")
    return bool(_AI_KEYWORDS.search(text_str))


def _derive_topic_key(title: str) -> str | None:
    title_lower = title.lower()
    for pattern, key in _TOPIC_PATTERNS:
        if re.search(pattern, title_lower):
            return key
    return None


async def _cluster_topics(db, article_rows: list[dict], analyses: list[dict], unique_raw) -> None:
    cutoff = (datetime.now(tz=timezone.utc) - timedelta(hours=72)).isoformat()
    for row, analysis, raw in zip(article_rows, analyses, unique_raw):
        topic_key = analysis.get("topic_key")
        if not topic_key:
            topic_key = _derive_topic_key(raw.title)
        if not topic_key:
            continue

        result = await db.execute(
            text(
                "SELECT id, article_count, heat_score FROM topics "
                "WHERE topic_key = :tk AND latest_at >= :cutoff LIMIT 1"
            ),
            {"tk": topic_key, "cutoff": cutoff},
        )
        existing = result.fetchone()
        heat = analysis.get("heat_score") or 0
        now_iso = datetime.now(tz=timezone.utc).isoformat()

        if existing:
            topic_id, count, old_heat = existing
            await db.execute(
                text("UPDATE topics SET article_count = :c, heat_score = :h, latest_at = :n WHERE id = :id"),
                {"c": count + 1, "h": max(old_heat, heat), "n": now_iso, "id": topic_id},
            )
        else:
            topic_id = str(uuid.uuid4())
            await db.execute(
                text(
                    "INSERT INTO topics (id, topic_key, title, summary, article_count, heat_score, "
                    "representative_id, first_seen_at, latest_at) VALUES "
                    "(:id, :tk, :title, :summary, 1, :heat, :rep, :now, :now)"
                ),
                {
                    "id": topic_id,
                    "tk": topic_key,
                    "title": raw.title,
                    "summary": analysis.get("summary"),
                    "heat": heat,
                    "rep": row["id"],
                    "now": now_iso,
                },
            )

        await db.execute(
            text("UPDATE articles SET topic_id = :tid WHERE id = :aid"),
            {"tid": topic_id, "aid": row["id"]},
        )


async def run_crawl_pipeline():
    crawlers = [RSSCrawler(), HackerNewsCrawler(), ArXivCrawler(), RedditCrawler()]
    all_raw = []
    for crawler in crawlers:
        try:
            results = await crawler.fetch()
            all_raw.extend(results)
        except Exception:
            pass

    ai_raw = [a for a in all_raw if _is_ai_related(a.title, a.content_snippet)]

    seen: set[str] = set()
    unique_raw = []
    for a in ai_raw:
        if a.original_url not in seen:
            seen.add(a.original_url)
            unique_raw.append(a)

    if not unique_raw:
        return 0

    if settings.anthropic_api_key:
        from app.analysis.claude_analyzer import analyze_batch
        analyses = await analyze_batch(unique_raw)
    else:
        analyses = [
            {
                "summary": None, "keywords": [], "category": "Other", "heat_score": 0,
                "topic_key": None, "paper_contribution": None, "readability_score": None,
            }
            for _ in unique_raw
        ]

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
            "paper_contribution": analysis.get("paper_contribution"),
            "readability_score": analysis.get("readability_score"),
        })

    async with AsyncSessionLocal() as db:
        for row in rows:
            await db.execute(
                text(
                    "INSERT OR IGNORE INTO articles "
                    "(id, title, source, source_type, original_url, published_at, crawled_at, "
                    "image_url, content_snippet, summary, keywords, category, heat_score, "
                    "paper_contribution, readability_score) "
                    "VALUES (:id, :title, :source, :source_type, :original_url, :published_at, :crawled_at, "
                    ":image_url, :content_snippet, :summary, :keywords, :category, :heat_score, "
                    ":paper_contribution, :readability_score)"
                ),
                row,
            )
        await _cluster_topics(db, rows, analyses, unique_raw)
        await db.commit()

    return len(rows)
