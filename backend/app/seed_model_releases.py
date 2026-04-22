import hashlib
import json

from sqlalchemy import text


def _deterministic_id(model_name: str, org: str, date: str) -> str:
    raw = f"{model_name}|{org}|{date}"
    h = hashlib.sha256(raw.encode()).hexdigest()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


SEED_DATA = [
    {
        "model_name": "GPT-4",
        "organization": "OpenAI",
        "release_date": "2023-03-14",
        "parameters_size": "~1.8T",
        "description": "OpenAI 首个大规模多模态模型，在专业和学术基准上展现人类水平表现",
        "benchmarks": {"MMLU": 86.4, "HumanEval": 67.0, "MATH": 42.5, "GSM8K": 92.0, "ARC": 96.3},
        "announcement_url": "https://openai.com/research/gpt-4",
        "category": "LLM",
    },
    {
        "model_name": "Llama 2 70B",
        "organization": "Meta",
        "release_date": "2023-07-18",
        "parameters_size": "70B",
        "description": "Meta 开源大语言模型第二代，推动开源 LLM 生态发展",
        "benchmarks": {"MMLU": 69.8, "HumanEval": 29.9, "MATH": 13.5, "GSM8K": 56.8},
        "announcement_url": "https://ai.meta.com/llama/",
        "category": "LLM",
    },
    {
        "model_name": "Gemini 1.0 Ultra",
        "organization": "Google",
        "release_date": "2023-12-06",
        "parameters_size": None,
        "description": "Google DeepMind 首款超越 GPT-4 的多模态模型",
        "benchmarks": {"MMLU": 90.0, "HumanEval": 74.4, "MATH": 53.2, "GSM8K": 94.4},
        "announcement_url": "https://deepmind.google/technologies/gemini/",
        "category": "multimodal",
    },
    {
        "model_name": "Gemini 1.5 Pro",
        "organization": "Google",
        "release_date": "2024-02-15",
        "parameters_size": None,
        "description": "百万 token 上下文窗口，长文档和视频理解能力突破",
        "benchmarks": {"MMLU": 85.9, "HumanEval": 71.9, "MATH": 58.5, "GSM8K": 91.7},
        "announcement_url": "https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/",
        "category": "multimodal",
    },
    {
        "model_name": "Mistral Large",
        "organization": "Mistral AI",
        "release_date": "2024-02-26",
        "parameters_size": None,
        "description": "Mistral 旗舰模型，欧洲 AI 力量的代表",
        "benchmarks": {"MMLU": 81.2, "MATH": 45.0},
        "announcement_url": "https://mistral.ai/news/mistral-large/",
        "category": "LLM",
    },
    {
        "model_name": "Claude 3 Opus",
        "organization": "Anthropic",
        "release_date": "2024-03-04",
        "parameters_size": None,
        "description": "Anthropic 旗舰模型，在推理、数学和编程方面表现突出",
        "benchmarks": {"MMLU": 86.8, "HumanEval": 84.9, "MATH": 60.1, "GSM8K": 95.0, "ARC": 96.4},
        "announcement_url": "https://www.anthropic.com/news/claude-3-family",
        "category": "LLM",
    },
    {
        "model_name": "Llama 3 70B",
        "organization": "Meta",
        "release_date": "2024-04-18",
        "parameters_size": "70B",
        "description": "Meta 第三代开源模型，训练数据量大幅提升至 15T tokens",
        "benchmarks": {"MMLU": 82.0, "HumanEval": 81.7, "MATH": 50.4, "GSM8K": 93.0},
        "announcement_url": "https://ai.meta.com/blog/meta-llama-3/",
        "category": "LLM",
    },
    {
        "model_name": "GPT-4o",
        "organization": "OpenAI",
        "release_date": "2024-05-13",
        "parameters_size": None,
        "description": "OpenAI 全能模型，原生支持文本、语音、图像多模态交互",
        "benchmarks": {"MMLU": 88.7, "HumanEval": 90.2, "MATH": 76.6},
        "announcement_url": "https://openai.com/index/hello-gpt-4o/",
        "category": "multimodal",
    },
    {
        "model_name": "Claude 3.5 Sonnet",
        "organization": "Anthropic",
        "release_date": "2024-06-20",
        "parameters_size": None,
        "description": "以中等规模超越前代旗舰模型，性价比突出",
        "benchmarks": {"MMLU": 88.7, "HumanEval": 92.0, "MATH": 71.1, "GSM8K": 96.4},
        "announcement_url": "https://www.anthropic.com/news/claude-3-5-sonnet",
        "category": "LLM",
    },
    {
        "model_name": "GPT-4o mini",
        "organization": "OpenAI",
        "release_date": "2024-07-18",
        "parameters_size": None,
        "description": "GPT-4o 的轻量版本，成本降低 60% 的同时保持高水准能力",
        "benchmarks": {"MMLU": 82.0, "HumanEval": 87.0, "MATH": 70.2, "GSM8K": 93.2},
        "announcement_url": "https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/",
        "category": "multimodal",
    },
    {
        "model_name": "Llama 3.1 405B",
        "organization": "Meta",
        "release_date": "2024-07-23",
        "parameters_size": "405B",
        "description": "最大开源模型，首次在多项基准上媲美闭源旗舰",
        "benchmarks": {"MMLU": 87.3, "HumanEval": 89.0, "MATH": 73.8, "GSM8K": 96.8},
        "announcement_url": "https://ai.meta.com/blog/meta-llama-3-1/",
        "category": "LLM",
    },
    {
        "model_name": "Mistral Large 2",
        "organization": "Mistral AI",
        "release_date": "2024-07-24",
        "parameters_size": "123B",
        "description": "Mistral 第二代旗舰，128K 上下文，代码和多语言能力飞跃",
        "benchmarks": {"MMLU": 84.0, "HumanEval": 92.0},
        "announcement_url": "https://mistral.ai/news/mistral-large-2407/",
        "category": "LLM",
    },
    {
        "model_name": "Qwen 2.5 72B",
        "organization": "Alibaba",
        "release_date": "2024-09-19",
        "parameters_size": "72B",
        "description": "通义千问新一代，中文能力领先，数学推理大幅提升",
        "benchmarks": {"MMLU": 85.3, "HumanEval": 86.4, "MATH": 83.1, "GSM8K": 95.8},
        "announcement_url": "https://qwenlm.github.io/blog/qwen2.5/",
        "category": "LLM",
    },
    {
        "model_name": "Claude 3.5 Sonnet (Oct)",
        "organization": "Anthropic",
        "release_date": "2024-10-22",
        "parameters_size": None,
        "description": "Claude 3.5 Sonnet 升级版，编程和工具使用能力再上台阶",
        "benchmarks": {"MMLU": 88.7, "HumanEval": 93.7, "MATH": 78.3, "GSM8K": 96.4},
        "announcement_url": "https://www.anthropic.com/news/3-5-models-and-computer-use",
        "category": "LLM",
    },
    {
        "model_name": "Gemini 2.0 Flash",
        "organization": "Google",
        "release_date": "2024-12-11",
        "parameters_size": None,
        "description": "下一代多模态模型，推理速度和工具调用能力大幅提升",
        "benchmarks": {"MMLU": 85.0, "HumanEval": 89.0, "MATH": 83.9},
        "announcement_url": "https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/",
        "category": "multimodal",
    },
    {
        "model_name": "DeepSeek-V3",
        "organization": "DeepSeek",
        "release_date": "2024-12-26",
        "parameters_size": "671B MoE",
        "description": "DeepSeek 开源 MoE 模型，以极低训练成本达到顶尖水平",
        "benchmarks": {"MMLU": 88.5, "HumanEval": 82.6, "MATH": 90.2, "GSM8K": 96.7},
        "announcement_url": "https://github.com/deepseek-ai/DeepSeek-V3",
        "category": "LLM",
    },
    {
        "model_name": "Gemini 2.5 Pro",
        "organization": "Google",
        "release_date": "2025-03-25",
        "parameters_size": None,
        "description": "Google 最强思考模型，原生多模态推理能力达到新高度",
        "benchmarks": {"MMLU": 89.8, "HumanEval": 93.0, "MATH": 86.5},
        "announcement_url": "https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/",
        "category": "multimodal",
    },
    {
        "model_name": "Claude 4 Opus",
        "organization": "Anthropic",
        "release_date": "2025-05-22",
        "parameters_size": None,
        "description": "Anthropic 新一代旗舰，Agent 和长上下文能力跃升",
        "benchmarks": {"MMLU": 90.4, "HumanEval": 95.2, "MATH": 83.6, "GSM8K": 97.8},
        "announcement_url": "https://www.anthropic.com/news/claude-4",
        "category": "LLM",
    },
]


async def seed_model_releases(conn):
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
        await conn.execute(
            text(
                "INSERT OR IGNORE INTO model_releases "
                "(id, model_name, organization, version, release_date, parameters_size, "
                "description, benchmarks, announcement_url, category) VALUES "
                "(:id, :model_name, :organization, :version, :release_date, :parameters_size, "
                ":description, :benchmarks, :announcement_url, :category)"
            ),
            row,
        )
