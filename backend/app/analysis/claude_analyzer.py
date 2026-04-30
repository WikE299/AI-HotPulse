import json
import re

from app.config import settings
from app.crawlers.base import RawArticle

BATCH_SIZE = 8  # articles per API call

_SYSTEM_PROMPT = """你是一个 AI 资讯分析助手。给定多篇文章的标题和内容片段，请为每篇文章输出一个 JSON 对象，包含以下字段：
- summary: 2-3 句中文摘要
- keywords: 5-8 个关键词数组（技术术语保留英文）
- category: LLM / CV / Robotics / Industry / Research / Other 之一
- heat_score: 1-10 整数热度评分
- topic_key: 规范化事件标识符（小写字母+连字符，如 "openai-gpt5-release"），无法归类时为 null
- paper_contribution: 仅当来源为学术论文时填写，一句话说明核心贡献；否则为 null
- readability_score: 仅学术论文时填写，1(需要PhD)-5(人人可读) 整数；否则为 null

输出一个 JSON 数组，每个元素对应一篇文章，顺序与输入一致。只输出 JSON，不要其他文字。"""


def _build_batch_content(articles: list[RawArticle]) -> str:
    parts = []
    for i, a in enumerate(articles):
        parts.append(
            f"[文章 {i + 1}]\n标题：{a.title}\n来源类型：{a.source_type}\n"
            f"内容片段：{a.content_snippet or '（无内容）'}"
        )
    return "\n\n".join(parts)


def _parse_json_array(raw: str) -> list[dict]:
    raw = re.sub(r"^```json\s*|```$", "", raw, flags=re.MULTILINE).strip()
    try:
        result = json.loads(raw)
        if isinstance(result, list):
            return result
        return [result]
    except json.JSONDecodeError:
        return []


_DUMMY = {
    "summary": None, "keywords": [], "category": "Other", "heat_score": 0,
    "topic_key": None, "paper_contribution": None, "readability_score": None,
}


async def _call_anthropic(system: str, user: str) -> str:
    import anthropic
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    message = await client.messages.create(
        model=settings.api_model,
        max_tokens=BATCH_SIZE * 400,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user}],
    )
    return message.content[0].text.strip()


async def _call_openai(system: str, user: str) -> str:
    from openai import AsyncOpenAI
    client = AsyncOpenAI(
        api_key=settings.openai_api_key,
        base_url=settings.api_base_url or None,
    )
    message = await client.chat.completions.create(
        model=settings.api_model,
        max_tokens=BATCH_SIZE * 400,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return message.choices[0].message.content.strip()


async def _call_llm(system: str, user: str) -> str:
    if settings.api_provider == "openai":
        return await _call_openai(system, user)
    return await _call_anthropic(system, user)


def _has_api_key() -> bool:
    if settings.api_provider == "openai":
        return bool(settings.openai_api_key)
    return bool(settings.anthropic_api_key)


async def analyze_batch(articles: list[RawArticle]) -> list[dict]:
    if not _has_api_key():
        return [_DUMMY.copy() for _ in articles]

    import asyncio
    semaphore = asyncio.Semaphore(3)
    results: list[dict] = []
    batches = [articles[i:i + BATCH_SIZE] for i in range(0, len(articles), BATCH_SIZE)]

    async def _analyze_batch(batch: list[RawArticle], batch_results: list[list[dict]], idx: int):
        async with semaphore:
            try:
                content = _build_batch_content(batch)
                raw = await _call_llm(_SYSTEM_PROMPT, content)
                parsed = _parse_json_array(raw)
                # Pad with dummies if response count doesn't match
                while len(parsed) < len(batch):
                    parsed.append(_DUMMY.copy())
                batch_results[idx] = parsed[:len(batch)]
            except Exception:
                batch_results[idx] = [_DUMMY.copy() for _ in batch]

    batch_results = [None] * len(batches)
    await asyncio.gather(*[_analyze_batch(b, batch_results, i) for i, b in enumerate(batches)])

    for batch_result in batch_results:
        results.extend(batch_result)
    return results
