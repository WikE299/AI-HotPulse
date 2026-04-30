"""Insert demo articles, topics, and a daily brief for UI preview."""
import sqlite3, uuid, json
from datetime import datetime, timedelta

DB = "hotpulse.db"
now = datetime.utcnow()

def ts(days_ago=0, hours_ago=0):
    return (now - timedelta(days=days_ago, hours=hours_ago)).strftime("%Y-%m-%d %H:%M:%S")

def uid():
    return str(uuid.uuid4())

conn = sqlite3.connect(DB)
c = conn.cursor()

# ── Topics ──
topics = [
    {"id": uid(), "topic_key": "openai-gpt5", "title": "OpenAI GPT-5 发布，多模态推理能力大幅飞跃",
     "summary": "OpenAI 正式发布 GPT-5，在推理、多模态理解和代码生成方面取得重大突破，MMLU 达到 92.3 分。",
     "article_count": 5, "heat_score": 10, "first_seen_at": ts(1), "latest_at": ts(0, 2)},
    {"id": uid(), "topic_key": "google-gemini", "title": "Google Gemini 2.5 Pro 实测：代码能力超越 GPT-4o",
     "summary": "Google DeepMind 发布 Gemini 2.5 Pro，在 100 万 token 上下文和代码生成方面表现突出。",
     "article_count": 4, "heat_score": 9, "first_seen_at": ts(2), "latest_at": ts(0, 5)},
    {"id": uid(), "topic_key": "ai-regulation", "title": "欧盟 AI Act 正式生效，全球监管格局重塑",
     "summary": "欧盟 AI 法案正式实施，对高风险 AI 系统提出严格合规要求，影响全球科技公司。",
     "article_count": 3, "heat_score": 7, "first_seen_at": ts(3), "latest_at": ts(1)},
    {"id": uid(), "topic_key": "anthropic-claude", "title": "Claude 4 Opus 发布：安全与能力的新平衡",
     "summary": "Anthropic 发布旗舰模型 Claude 4 Opus，在复杂推理和安全对齐方面树立新标杆。",
     "article_count": 3, "heat_score": 9, "first_seen_at": ts(2), "latest_at": ts(0, 8)},
]

for t in topics:
    c.execute("""INSERT OR IGNORE INTO topics
        (id, topic_key, title, summary, article_count, heat_score, representative_id, first_seen_at, latest_at)
        VALUES (?,?,?,?,?,?,NULL,?,?)""",
        (t["id"], t["topic_key"], t["title"], t["summary"],
         t["article_count"], t["heat_score"], t["first_seen_at"], t["latest_at"]))

# ── Articles ──
articles = [
    # GPT-5 topic
    {"title": "OpenAI 正式发布 GPT-5：推理能力实现代际飞跃", "source": "机器之心", "source_type": "chinese",
     "url": "https://example.com/gpt5-release", "summary": "OpenAI 今日正式发布了 GPT-5 模型，在数学推理、代码生成、多模态理解等多项基准上大幅领先前代。MMLU 达到 92.3，HumanEval 达到 93.1。",
     "keywords": ["GPT-5", "OpenAI", "LLM", "多模态", "推理"], "category": "LLM", "heat_score": 10,
     "topic_key": "openai-gpt5", "days_ago": 0, "hours_ago": 2},
    {"title": "GPT-5 技术报告深度解读：架构创新与训练细节", "source": "量子位", "source_type": "chinese",
     "url": "https://example.com/gpt5-tech", "summary": "GPT-5 技术报告揭示了 MoE 架构升级、RLHF 改进和全新的推理链训练方法，本文逐一解读关键技术突破。",
     "keywords": ["GPT-5", "技术报告", "MoE", "RLHF"], "category": "Research", "heat_score": 9,
     "topic_key": "openai-gpt5", "days_ago": 0, "hours_ago": 4},
    {"title": "GPT-5 vs Claude 4 vs Gemini 2.5: 三大旗舰模型全面对比", "source": "36氪", "source_type": "chinese",
     "url": "https://example.com/model-compare", "summary": "我们对三大最新旗舰模型进行了全面评测，涵盖推理、编程、创意写作和多语言能力四大维度。",
     "keywords": ["GPT-5", "Claude 4", "Gemini 2.5", "模型评测"], "category": "LLM", "heat_score": 9,
     "topic_key": "openai-gpt5", "days_ago": 0, "hours_ago": 6},
    {"title": "OpenAI Announces GPT-5 with Breakthrough Reasoning", "source": "TechCrunch", "source_type": "english",
     "url": "https://example.com/tc-gpt5", "summary": "OpenAI has released GPT-5, its most advanced model featuring significantly improved reasoning, multimodal understanding, and code generation capabilities.",
     "keywords": ["GPT-5", "OpenAI", "reasoning", "AI"], "category": "LLM", "heat_score": 8,
     "topic_key": "openai-gpt5", "days_ago": 0, "hours_ago": 3},

    # Gemini topic
    {"title": "Gemini 2.5 Pro 实测：100万 token 上下文到底有多强", "source": "机器之心", "source_type": "chinese",
     "url": "https://example.com/gemini-test", "summary": "Google DeepMind 的 Gemini 2.5 Pro 支持 100 万 token 上下文窗口。我们用长文档摘要、代码库理解等任务进行了深度测试。",
     "keywords": ["Gemini 2.5", "Google", "长上下文", "评测"], "category": "LLM", "heat_score": 8,
     "topic_key": "google-gemini", "days_ago": 1, "hours_ago": 0},
    {"title": "Google DeepMind: Gemini 2.5 Sets New Coding Benchmarks", "source": "The Verge", "source_type": "english",
     "url": "https://example.com/verge-gemini", "summary": "Google's latest Gemini 2.5 Pro model achieves state-of-the-art results on SWE-bench and HumanEval, surpassing GPT-4o in code generation tasks.",
     "keywords": ["Gemini 2.5", "coding", "benchmark", "Google"], "category": "LLM", "heat_score": 7,
     "topic_key": "google-gemini", "days_ago": 2, "hours_ago": 0},

    # Claude topic
    {"title": "Anthropic 发布 Claude 4 Opus：安全与智能的新平衡点", "source": "量子位", "source_type": "chinese",
     "url": "https://example.com/claude4-release", "summary": "Anthropic 正式发布 Claude 4 Opus，在维持业界领先安全性的同时，推理和编程能力大幅提升，MMLU 达到 91.8。",
     "keywords": ["Claude 4", "Anthropic", "安全AI", "推理"], "category": "LLM", "heat_score": 9,
     "topic_key": "anthropic-claude", "days_ago": 1, "hours_ago": 5},

    # Regulation topic
    {"title": "欧盟 AI Act 今日正式生效：对中国企业意味着什么", "source": "36氪", "source_type": "chinese",
     "url": "https://example.com/eu-ai-act", "summary": "欧盟 AI 法案正式实施，高风险 AI 系统需在 6 个月内完成合规。中国出海企业面临新的监管挑战。",
     "keywords": ["AI法案", "欧盟", "监管", "合规"], "category": "Industry", "heat_score": 7,
     "topic_key": "ai-regulation", "days_ago": 2, "hours_ago": 0},

    # Standalone articles (no topic)
    {"title": "Scaling Laws 遇到瓶颈？新研究提出 Inference-Time Compute 范式", "source": "ArXiv", "source_type": "academic",
     "url": "https://arxiv.org/abs/2026.12345", "summary": "研究者发现传统 Scaling Laws 在超大规模模型上出现收益递减，提出在推理阶段分配更多计算资源的新范式。",
     "keywords": ["Scaling Laws", "推理计算", "效率"], "category": "Research", "heat_score": 8,
     "paper_contribution": "提出 Inference-Time Compute Scaling 框架，在固定训练预算下提升推理质量", "readability_score": 3,
     "topic_key": None, "days_ago": 0, "hours_ago": 8},
    {"title": "Diffusion Transformer 在视频生成中的最新进展", "source": "ArXiv", "source_type": "academic",
     "url": "https://arxiv.org/abs/2026.12346", "summary": "综述论文梳理了 Diffusion Transformer 在视频生成领域的演进路线，从 Sora 到最新的开源方案。",
     "keywords": ["DiT", "视频生成", "Sora", "扩散模型"], "category": "CV", "heat_score": 6,
     "paper_contribution": "系统梳理 DiT 架构在视频生成中的应用，提出统一的评估框架", "readability_score": 4,
     "topic_key": None, "days_ago": 1, "hours_ago": 3},
    {"title": "斯坦福团队开源机器人基础模型 RT-3", "source": "机器之心", "source_type": "chinese",
     "url": "https://example.com/rt3-release", "summary": "斯坦福大学发布开源机器人基础模型 RT-3，能够在零样本条件下完成复杂操作任务，代码和权重已开放。",
     "keywords": ["RT-3", "机器人", "基础模型", "开源"], "category": "Robotics", "heat_score": 7,
     "topic_key": None, "days_ago": 1, "hours_ago": 6},
    {"title": "AI Agent 框架大战：LangGraph vs CrewAI vs AutoGen 实战对比", "source": "HackerNews", "source_type": "english",
     "url": "https://example.com/agent-compare", "summary": "A comprehensive comparison of the three leading AI agent frameworks, testing them on real-world tasks including web research, code generation, and data analysis.",
     "keywords": ["AI Agent", "LangGraph", "CrewAI", "AutoGen"], "category": "LLM", "heat_score": 7,
     "topic_key": None, "days_ago": 0, "hours_ago": 10},
    {"title": "Reddit 热议：GPT-5 是否真的实现了 AGI 的第一步", "source": "Reddit", "source_type": "social",
     "url": "https://example.com/reddit-gpt5-agi", "summary": "Reddit r/MachineLearning 社区围绕 GPT-5 是否代表通向 AGI 的重要里程碑展开了激烈讨论。",
     "keywords": ["AGI", "GPT-5", "讨论", "Reddit"], "category": "Industry", "heat_score": 6,
     "topic_key": "openai-gpt5", "days_ago": 0, "hours_ago": 5},
    {"title": "小模型的逆袭：Phi-4 Mini 以 3.8B 参数达到 GPT-3.5 水平", "source": "The Verge", "source_type": "english",
     "url": "https://example.com/phi4-mini", "summary": "Microsoft Research 发布 Phi-4 Mini，仅 3.8B 参数就在多项基准上匹配 GPT-3.5 Turbo，开启端侧部署新时代。",
     "keywords": ["Phi-4", "小模型", "端侧部署", "Microsoft"], "category": "LLM", "heat_score": 7,
     "topic_key": None, "days_ago": 2, "hours_ago": 0},
    {"title": "NVIDIA H200 GPU 全球缺货加剧，AI 训练成本持续攀升", "source": "36氪", "source_type": "chinese",
     "url": "https://example.com/h200-shortage", "summary": "NVIDIA H200 GPU 供不应求导致云计算平台算力紧张，头部 AI 公司纷纷转向自研芯片加速战略。",
     "keywords": ["NVIDIA", "H200", "GPU", "算力", "芯片"], "category": "Industry", "heat_score": 6,
     "topic_key": None, "days_ago": 3, "hours_ago": 0},
]

topic_id_map = {t["topic_key"]: t["id"] for t in topics}

for a in articles:
    aid = uid()
    tid = topic_id_map.get(a.get("topic_key")) if a.get("topic_key") else None
    pub = ts(a["days_ago"], a["hours_ago"])
    c.execute("""INSERT OR IGNORE INTO articles
        (id, title, source, source_type, original_url, published_at, crawled_at,
         image_url, summary, keywords, category, heat_score, content_snippet,
         paper_contribution, readability_score, topic_id)
        VALUES (?,?,?,?,?,?,?,NULL,?,?,?,?,?,?,?,?)""",
        (aid, a["title"], a["source"], a["source_type"], a["url"], pub, pub,
         a["summary"], json.dumps(a["keywords"], ensure_ascii=False),
         a["category"], a["heat_score"], a["summary"],
         a.get("paper_contribution"), a.get("readability_score"), tid))

# Update representative_id for topics
for t in topics:
    c.execute("""UPDATE topics SET representative_id = (
        SELECT id FROM articles WHERE topic_id = ? ORDER BY heat_score DESC LIMIT 1
    ) WHERE id = ?""", (t["id"], t["id"]))

# ── Daily Brief ──
today = now.strftime("%Y-%m-%d")
brief_content = f"""# AI 热点日报 — {today}

## 🔥 头条

**OpenAI GPT-5 正式发布** — OpenAI 今日发布了其最新旗舰模型 GPT-5，在推理、多模态理解和代码生成等多项基准上实现代际飞跃。MMLU 达到 92.3，HumanEval 达到 93.1，创下新的 SOTA。

## 📊 重点关注

### 模型发布
- **GPT-5** 发布，推理能力大幅提升，支持原生多模态输入
- **Claude 4 Opus** 发布，在安全对齐和复杂推理间取得新平衡
- **Gemini 2.5 Pro** 实测表现优异，100 万 token 上下文窗口令人印象深刻

### 研究进展
- Inference-Time Compute 成为新趋势，Scaling Laws 遭遇瓶颈后的新方向
- Diffusion Transformer 在视频生成中持续推进
- 斯坦福开源机器人基础模型 RT-3

### 行业动态
- 欧盟 AI Act 正式生效，全球 AI 监管进入新阶段
- NVIDIA H200 GPU 全球缺货，AI 算力竞争白热化
- Phi-4 Mini 以 3.8B 参数达到 GPT-3.5 水平，端侧 AI 前景广阔

## 💡 今日洞察

本周是 AI 行业的「超级周」，三大旗舰模型集中发布。GPT-5 的推理飞跃、Claude 4 的安全突破、Gemini 2.5 的长上下文能力，标志着 LLM 竞争进入了多维度比拼的新阶段。与此同时，小模型（Phi-4 Mini）在效率上的突破表明，AI 的未来不仅是更大，更是更智能。

---
*由 AI HotPulse 自动生成 · {today}*
"""

brief_id = uid()
c.execute("""INSERT OR IGNORE INTO daily_briefs (id, date, content, article_ids, generated_at)
    VALUES (?,?,?,?,?)""",
    (brief_id, today, brief_content, "[]", ts(0)))

conn.commit()
print(f"Done: Inserted {len(topics)} topics, {len(articles)} articles, 1 daily brief")
conn.close()
