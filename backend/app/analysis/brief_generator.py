async def generate_daily_brief(date: str, articles: list) -> str:
    from app.config import settings
    from app.analysis.claude_analyzer import _has_api_key, _call_llm
    if _has_api_key():
        return await _ai_brief(date, articles)
    return _template_brief(date, articles)


def _template_brief(date: str, articles: list) -> str:
    top = articles[:3]
    academic = [a for a in articles if getattr(a, "source_type", None) == "academic"][:2]

    lines = [f"# AI HotPulse · {date} 每日简报\n"]

    lines.append("## 🔥 今日重点\n")
    for i, a in enumerate(top, 1):
        summary = getattr(a, "summary", None) or "（暂无摘要）"
        url = getattr(a, "original_url", "#")
        lines.append(f"**{i}. {a.title}**\n\n{summary}\n\n[阅读原文]({url})\n")

    if academic:
        lines.append("## 📄 论文亮点\n")
        for a in academic:
            contrib = getattr(a, "paper_contribution", None) or getattr(a, "summary", None) or "（暂无摘要）"
            url = getattr(a, "original_url", "#")
            lines.append(f"- **{a.title}**\n\n  {contrib}\n\n  [查看论文]({url})\n")

    lines.append("## 💡 今日洞察\n")
    lines.append("AI 技术迭代加速，大模型能力持续扩展，保持关注前沿动态，把握发展脉络。\n")

    return "\n".join(lines)


async def _ai_brief(date: str, articles: list) -> str:
    from app.analysis.claude_analyzer import _call_llm

    articles_text = "\n\n".join(
        f"[{i + 1}] {a.title}\n来源：{getattr(a, 'source', '未知')}（{getattr(a, 'source_type', '未知')}）\n摘要：{getattr(a, 'summary', None) or '无'}"
        for i, a in enumerate(articles[:15])
    )

    prompt = f"""请根据以下 {min(len(articles), 15)} 篇 AI 文章，生成一份 {date} 的每日 AI 简报，使用 Markdown 格式，包含：

## 🔥 三大核心事件
（3 条，每条 2-3 句话，说明事件意义）

## 📄 论文亮点
（最多 2 条，仅来源类型为 academic 的文章，说明核心贡献；若无学术文章则省略此节）

## 💡 今日一句话洞察
（1 句话，点明今日 AI 圈最重要的趋势）

文章列表：
{articles_text}

只输出 Markdown 正文，不要额外说明。"""

    system = "你是一个专业的 AI 资讯编辑，擅长撰写简洁有力的每日简报。"
    return await _call_llm(system, prompt)
