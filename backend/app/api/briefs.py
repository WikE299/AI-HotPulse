import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.brief import DailyBrief
from app.models.article import Article

router = APIRouter()


@router.get("/briefs/latest")
async def latest_brief(db: AsyncSession = Depends(get_db)):
    stmt = select(DailyBrief).order_by(desc(DailyBrief.date)).limit(1)
    brief = (await db.scalars(stmt)).first()
    if not brief:
        raise HTTPException(status_code=404, detail="No briefs yet")
    return _serialize(brief)


@router.get("/briefs/{date}")
async def get_brief(date: str, db: AsyncSession = Depends(get_db)):
    stmt = select(DailyBrief).where(DailyBrief.date == date)
    brief = (await db.scalars(stmt)).first()
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    return _serialize(brief)


@router.post("/briefs/generate")
async def generate_brief(db: AsyncSession = Depends(get_db)):
    from app.analysis.brief_generator import generate_daily_brief

    today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

    existing = (await db.scalars(
        select(DailyBrief).where(DailyBrief.date == today)
    )).first()
    if existing:
        return _serialize(existing)

    articles = (await db.scalars(
        select(Article)
        .order_by(desc(Article.heat_score), desc(Article.published_at))
        .limit(20)
    )).all()

    if not articles:
        raise HTTPException(status_code=404, detail="No articles to generate brief from")

    content = await generate_daily_brief(today, list(articles))
    brief = DailyBrief(
        id=str(uuid.uuid4()),
        date=today,
        content=content,
        article_ids=json.dumps([a.id for a in articles]),
        generated_at=datetime.now(tz=timezone.utc),
    )
    db.add(brief)
    await db.commit()
    await db.refresh(brief)
    return _serialize(brief)


def _serialize(b: DailyBrief) -> dict:
    return {
        "id": b.id,
        "date": b.date,
        "content": b.content,
        "article_ids": b.article_ids,
        "generated_at": b.generated_at.isoformat() if b.generated_at else None,
    }
