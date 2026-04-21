import json
import re

import anthropic

from app.config import settings
from app.crawlers.base import RawArticle

_client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

_SYSTEM_PROMPT = """你是一个 AI 资讯分析助手。给定一篇文章的标题和内容片段，请输出一个 JSON 对象，包含以下字段：
- summary: 2-3 句中文摘要，简明扼要说明文章核心内容
- keywords: 5-8 个中文关键词的数组（技术术语保留英文）
- category: 分类，只能是以下之一：LLM / CV / Robotics / Industry / Research / Other
- heat_score: 1-10 整数热度评分（10 最热，基于话题重要性和新颖性）

只输出 JSON，不要其他文字。"""


async def analyze_article(article: RawArticle) -> dict:
    content = f"标题：{article.title}\n\n内容片段：{article.content_snippet or '（无内容）'}"
    message = await _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=[
            {
                "type": "text",
                "text": _SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": content}],
    )
    raw = message.content[0].text.strip()
    raw = re.sub(r"^```json\s*|```$", "", raw, flags=re.MULTILINE).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"summary": None, "keywords": [], "category": "Other", "heat_score": 0}


async def analyze_batch(articles: list[RawArticle]) -> list[dict]:
    import asyncio
    semaphore = asyncio.Semaphore(5)

    async def _analyze(a: RawArticle) -> dict:
        async with semaphore:
            return await analyze_article(a)

    return await asyncio.gather(*[_analyze(a) for a in articles])
