# AI HotPulse

AI 热点脉搏 — 追踪 AI 领域最前沿的资讯、论文和模型动态。

## 功能

- **热点文章流** — 聚合 ArXiv、HackerNews、Reddit、RSS 等多源 AI 资讯，按热度排序
- **论文速读** — 学术论文摘要与贡献点提取，快速掌握核心观点
- **话题聚合** — 自动识别热点话题（GPT-5、Gemini、Claude 等），追踪事件脉络
- **每日简报** — AI 自动生成的每日热点摘要
- **模型动态** — 旗舰模型发布时间线 + 性能排行榜（Arena）
- **Oracle 预测** — 浮动卡片展示 AI 领域趋势预测

## 技术栈

| 层 | 技术 |
|---|------|
| 前端 | React 19 + TypeScript + Vite + Recharts |
| 后端 | Python + FastAPI + SQLAlchemy + aiosqlite |
| AI 分析 | Anthropic Claude API |
| 数据采集 | ArXiv / HackerNews / Reddit / RSS 爬虫 |
| 定时任务 | APScheduler |
| 部署 | Vercel (前端) + Render (后端) |

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+

### 后端

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env，填入 ANTHROPIC_API_KEY（可选，不填则跳过 AI 分析）

uvicorn main:app --reload --port 8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

### Docker

```bash
# 需要先设置环境变量
export ANTHROPIC_API_KEY=your_key_here
docker compose up
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ANTHROPIC_API_KEY` | Claude API Key，用于文章分析（可选） | 空 |
| `DATABASE_URL` | 数据库连接串 | `sqlite+aiosqlite:///./hotpulse.db` |
| `CORS_ORIGINS` | 允许的前端域名 | `http://localhost:5173` |
| `CRAWL_SCHEDULE_HOUR` | 每日爬取时间（时） | `8` |
| `CRAWL_SCHEDULE_MINUTE` | 每日爬取时间（分） | `0` |
| `VITE_API_URL` | 前端 API 地址 | `http://localhost:8000/api` |

## 项目结构

```
AI-HotPulse
├── backend/
│   ├── app/
│   │   ├── api/           # API 路由
│   │   ├── analysis/      # Claude AI 分析
│   │   ├── crawlers/      # 数据爬虫（ArXiv/HN/Reddit/RSS）
│   │   ├── models/        # 数据模型
│   │   ├── config.py      # 配置
│   │   ├── database.py    # 数据库初始化
│   │   ├── pipeline.py    # 爬取-分析流水线
│   │   └── scheduler.py   # 定时任务
│   ├── main.py            # FastAPI 入口
│   ├── seed_demo.py       # Demo 数据
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/         # 页面组件
│   │   ├── components/    # 通用组件
│   │   ├── api/           # API 调用
│   │   └── utils/         # 工具函数
│   └── package.json
├── docker-compose.yml
├── render.yaml            # Render 部署配置
└── vercel.json            # Vercel 部署配置
```

## License

MIT
