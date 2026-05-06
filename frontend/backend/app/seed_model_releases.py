import hashlib
import json

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from app.models.model_release import ModelRelease


def _deterministic_id(model_name: str, org: str, date: str) -> str:
    raw = f"{model_name}|{org}|{date}"
    h = hashlib.sha256(raw.encode()).hexdigest()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


SEED_DATA = [
    # ── OpenAI ──
    {
        "model_name": "GPT-4o",
        "organization": "OpenAI",
        "release_date": "2024-05-13",
        "parameters_size": None,
        "description": "全能多模态模型，原生支持文本、语音、图像交互",
        "benchmarks": {"MMLU": 88.7, "HumanEval": 90.2, "MATH": 76.6, "GSM8K": 95.8, "ARC": 96.7},
        "announcement_url": "https://openai.com/index/hello-gpt-4o/",
        "category": "multimodal",
    },
    {
        "model_name": "o3",
        "organization": "OpenAI",
        "release_date": "2025-04-16",
        "parameters_size": None,
        "description": "OpenAI 最强推理模型，思维链推理能力达到新高度",
        "benchmarks": {"MMLU": 92.3, "HumanEval": 96.8, "MATH": 96.7, "GSM8K": 98.4, "ARC": 98.8},
        "announcement_url": "https://openai.com/index/o3-and-o4-mini/",
        "category": "LLM",
    },
    {
        "model_name": "GPT-4.1",
        "organization": "OpenAI",
        "release_date": "2025-04-14",
        "parameters_size": None,
        "description": "GPT-4o 继任者，指令遵循和长上下文能力大幅提升",
        "benchmarks": {"MMLU": 90.2, "HumanEval": 94.5, "MATH": 82.1, "GSM8K": 97.0, "ARC": 97.5},
        "announcement_url": "https://openai.com/index/gpt-4-1/",
        "category": "LLM",
    },
    # ── Anthropic ──
    {
        "model_name": "Claude 3.5 Sonnet",
        "organization": "Anthropic",
        "release_date": "2024-10-22",
        "parameters_size": None,
        "description": "编程和工具使用能力突出的中端模型",
        "benchmarks": {"MMLU": 88.7, "HumanEval": 93.7, "MATH": 78.3, "GSM8K": 96.4, "ARC": 96.2},
        "announcement_url": "https://www.anthropic.com/news/3-5-models-and-computer-use",
        "category": "LLM",
    },
    {
        "model_name": "Claude Sonnet 4",
        "organization": "Anthropic",
        "release_date": "2025-05-22",
        "parameters_size": None,
        "description": "Anthropic 新一代中端模型，Agent 能力和代码生成跃升",
        "benchmarks": {"MMLU": 90.1, "HumanEval": 95.0, "MATH": 83.0, "GSM8K": 97.5, "ARC": 97.0},
        "announcement_url": "https://www.anthropic.com/news/claude-4",
        "category": "LLM",
    },
    {
        "model_name": "Claude Opus 4",
        "organization": "Anthropic",
        "release_date": "2025-05-22",
        "parameters_size": None,
        "description": "Anthropic 旗舰模型，长上下文推理和复杂任务处理能力最强",
        "benchmarks": {"MMLU": 91.5, "HumanEval": 96.2, "MATH": 85.5, "GSM8K": 98.0, "ARC": 97.8},
        "announcement_url": "https://www.anthropic.com/news/claude-4",
        "category": "LLM",
    },
    # ── Google ──
    {
        "model_name": "Gemini 2.5 Pro",
        "organization": "Google",
        "release_date": "2025-03-25",
        "parameters_size": None,
        "description": "Google 最强思考模型，原生多模态推理达到新高度",
        "benchmarks": {"MMLU": 89.8, "HumanEval": 93.0, "MATH": 86.5, "GSM8K": 97.2, "ARC": 97.0},
        "announcement_url": "https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/",
        "category": "multimodal",
    },
    {
        "model_name": "Gemini 2.5 Flash",
        "organization": "Google",
        "release_date": "2025-04-09",
        "parameters_size": None,
        "description": "高性价比思考模型，速度和能力的最优平衡",
        "benchmarks": {"MMLU": 87.5, "HumanEval": 90.0, "MATH": 82.0, "GSM8K": 95.5, "ARC": 95.8},
        "announcement_url": "https://blog.google/technology/google-deepmind/gemini-2-5-flash/",
        "category": "multimodal",
    },
    # ── Meta ──
    {
        "model_name": "Llama 4 Maverick",
        "organization": "Meta",
        "release_date": "2025-04-05",
        "parameters_size": "400B MoE",
        "description": "Meta 最新旗舰开源模型，MoE 架构，128K 上下文",
        "benchmarks": {"MMLU": 88.0, "HumanEval": 91.5, "MATH": 78.0, "GSM8K": 95.0, "ARC": 96.0},
        "announcement_url": "https://ai.meta.com/blog/llama-4-multimodal-intelligence/",
        "category": "LLM",
    },
    {
        "model_name": "Llama 4 Scout",
        "organization": "Meta",
        "release_date": "2025-04-05",
        "parameters_size": "109B MoE",
        "description": "轻量级开源 MoE 模型，10M token 超长上下文",
        "benchmarks": {"MMLU": 85.0, "HumanEval": 88.0, "MATH": 72.0, "GSM8K": 93.0, "ARC": 94.5},
        "announcement_url": "https://ai.meta.com/blog/llama-4-multimodal-intelligence/",
        "category": "LLM",
    },
    # ── DeepSeek ──
    {
        "model_name": "DeepSeek-R1",
        "organization": "DeepSeek",
        "release_date": "2025-01-20",
        "parameters_size": "671B MoE",
        "description": "开源推理模型，通过强化学习训练思维链，数学和代码能力媲美 o1",
        "benchmarks": {"MMLU": 90.8, "HumanEval": 92.0, "MATH": 97.3, "GSM8K": 97.8, "ARC": 97.5},
        "announcement_url": "https://github.com/deepseek-ai/DeepSeek-R1",
        "category": "LLM",
    },
    {
        "model_name": "DeepSeek-V3",
        "organization": "DeepSeek",
        "release_date": "2024-12-26",
        "parameters_size": "671B MoE",
        "description": "以极低训练成本达到顶尖水平的开源 MoE 模型",
        "benchmarks": {"MMLU": 88.5, "HumanEval": 82.6, "MATH": 90.2, "GSM8K": 96.7, "ARC": 95.0},
        "announcement_url": "https://github.com/deepseek-ai/DeepSeek-V3",
        "category": "LLM",
    },
    # ── Alibaba ──
    {
        "model_name": "Qwen3 235B",
        "organization": "Alibaba",
        "release_date": "2025-04-28",
        "parameters_size": "235B MoE",
        "description": "通义千问旗舰 MoE 模型，支持思考模式切换，中英文能力领先",
        "benchmarks": {"MMLU": 89.0, "HumanEval": 91.0, "MATH": 90.0, "GSM8K": 96.5, "ARC": 96.0},
        "announcement_url": "https://qwenlm.github.io/blog/qwen3/",
        "category": "LLM",
    },
    # ── Mistral ──
    {
        "model_name": "Mistral Large 2",
        "organization": "Mistral AI",
        "release_date": "2024-07-24",
        "parameters_size": "123B",
        "description": "欧洲 AI 旗舰，128K 上下文，代码和多语言能力突出",
        "benchmarks": {"MMLU": 84.0, "HumanEval": 92.0, "MATH": 69.0, "GSM8K": 93.5, "ARC": 94.0},
        "announcement_url": "https://mistral.ai/news/mistral-large-2407/",
        "category": "LLM",
    },
    # ── xAI ──
    {
        "model_name": "Grok-3",
        "organization": "xAI",
        "release_date": "2025-02-17",
        "parameters_size": None,
        "description": "xAI 旗舰模型，20 万 GPU 集群训练，推理能力强劲",
        "benchmarks": {"MMLU": 90.0, "HumanEval": 93.5, "MATH": 89.0, "GSM8K": 97.0, "ARC": 97.2},
        "announcement_url": "https://x.ai/news/grok-3",
        "category": "LLM",
    },
]


async def seed_model_releases(conn):
    dialect_name = conn.dialect.name
    for entry in SEED_DATA:
        row = {
            "id": _deterministic_id(entry["model_name"], entry["organization"], entry["release_date"]),
            "model_name": entry["model_name"],
            "organization": entry["organization"],
            "version": entry.get("version"),
            "release_date": entry["release_date"],
            "parameters_size": entry.get("parameters_size"),
            "description": entry.get("description"),
            "benchmarks": json.dumps(entry.get("benchmarks") or {}),
            "announcement_url": entry.get("announcement_url"),
            "category": entry.get("category", "LLM"),
        }
        if dialect_name == "postgresql":
            stmt = pg_insert(ModelRelease).values(**row).on_conflict_do_nothing(
                index_elements=[ModelRelease.id]
            )
        else:
            stmt = sqlite_insert(ModelRelease).values(**row).on_conflict_do_nothing(
                index_elements=[ModelRelease.id]
            )
        await conn.execute(stmt)
