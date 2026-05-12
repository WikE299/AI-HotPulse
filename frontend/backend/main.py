import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.api import articles, admin, topics, briefs, model_releases, predictions
from app.scheduler import start_scheduler, shutdown_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await asyncio.wait_for(init_db(), timeout=8)
    except Exception as e:
        import logging
        logging.error(f"init_db failed: {e}")
    if settings.enable_scheduler:
        start_scheduler()
    yield
    if settings.enable_scheduler:
        shutdown_scheduler()


app = FastAPI(title="AI-HotPulse API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(topics.router, prefix="/api")
app.include_router(briefs.router, prefix="/api")
app.include_router(model_releases.router, prefix="/api")
app.include_router(predictions.router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
