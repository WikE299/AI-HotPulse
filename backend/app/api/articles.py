import uuid
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.article import Article

router = APIRouter()


@router.get("/articles")
async def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    source_type: Optional[str] = None,
    category: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Article).order_by(desc(Article.published_at), desc(Article.heat_score))

    if source_type:
        stmt = stmt.where(Article.source_type == source_type)
    if category:
        stmt = stmt.where(Article.category == category)
    if date_from:
        stmt = stmt.where(Article.published_at >= date_from)
    if date_to:
        from datetime import datetime, timezone, timedelta
        end = datetime.combine(date_to, datetime.max.time()).replace(tzinfo=timezone.utc)
        stmt = stmt.where(Article.published_at <= end)

    total_result = await db.scalars(select(Article.id).order_by(None).where(
        *([Article.source_type == source_type] if source_type else []),
        *([Article.category == category] if category else []),
    ))

    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)
    articles = (await db.scalars(stmt)).all()

    return {
        "items": [_serialize(a) for a in articles],
        "page": page,
        "page_size": page_size,
    }


@router.get("/articles/{article_id}")
async def get_article(article_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    article = await db.get(Article, article_id)
    if not article:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Article not found")
    return _serialize(article)


def _serialize(a: Article) -> dict:
    return {
        "id": str(a.id),
        "title": a.title,
        "source": a.source,
        "source_type": a.source_type,
        "original_url": a.original_url,
        "published_at": a.published_at.isoformat() if a.published_at else None,
        "image_url": a.image_url,
        "summary": a.summary,
        "keywords": a.keywords or [],
        "category": a.category,
        "heat_score": a.heat_score,
        "content_snippet": a.content_snippet,
    }
