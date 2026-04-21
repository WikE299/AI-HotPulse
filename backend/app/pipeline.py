from datetime import datetime, timezone
import json
import re

from sqlalchemy import text

from app.config import settings
from app.crawlers.arxiv import ArXivCrawler
from app.crawlers.hackernews import HackerNewsCrawler
from app.crawlers.reddit import RedditCrawler
from app.crawlers.rss_crawler import RSSCrawler
from app.database import AsyncSessionLocal

# Must match at least one keyword to be considered AI-related
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


def _is_ai_related(title: str, snippet: str | None) -> bool:
    text = (title or "") + " " + (snippet or "")
    return bool(_AI_KEYWORDS.search(text))


async def run_crawl_pipeline():
    crawlers = [RSSCrawler(), HackerNewsCrawler(), ArXivCrawler(), RedditCrawler()]
    all_raw = []
    for crawler in crawlers:
        try:
            results = await crawler.fetch()
            all_raw.extend(results)
        except Exception:
            pass

    # Keep only AI-related articles
    ai_raw = [a for a in all_raw if _is_ai_related(a.title, a.content_snippet)]

    # Deduplicate within batch
    seen: set[str] = set()
    unique_raw = []
    for a in ai_raw:
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
