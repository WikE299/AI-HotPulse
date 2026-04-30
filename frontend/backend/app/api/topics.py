from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.topic import Topic
from app.models.article import Article

router = APIRouter()


@router.get("/topics")
async def list_topics(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * page_size
    stmt = select(Topic).order_by(desc(Topic.latest_at)).offset(offset).limit(page_size)
    topics = (await db.scalars(stmt)).all()
    return {
        "items": [_serialize_topic(t) for t in topics],
        "page": page,
        "page_size": page_size,
    }


@router.get("/topics/{topic_id}")
async def get_topic(topic_id: str, db: AsyncSession = Depends(get_db)):
    topic = await db.get(Topic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    articles_stmt = (
        select(Article)
        .where(Article.topic_id == topic_id)
        .order_by(desc(Article.published_at))
    )
    articles = (await db.scalars(articles_stmt)).all()

    return {
        **_serialize_topic(topic),
        "articles": [_serialize_article(a) for a in articles],
    }


def _serialize_topic(t: Topic) -> dict:
    return {
        "id": t.id,
        "topic_key": t.topic_key,
        "title": t.title,
        "summary": t.summary,
        "article_count": t.article_count,
        "heat_score": t.heat_score,
        "representative_id": t.representative_id,
        "first_seen_at": t.first_seen_at.isoformat() if t.first_seen_at else None,
        "latest_at": t.latest_at.isoformat() if t.latest_at else None,
    }


def _serialize_article(a: Article) -> dict:
    return {
        "id": a.id,
        "title": a.title,
        "source": a.source,
        "source_type": a.source_type,
        "original_url": a.original_url,
        "published_at": a.published_at.isoformat() if a.published_at else None,
        "summary": a.summary,
        "heat_score": a.heat_score,
        "keywords": a.keywords or [],
        "category": a.category,
        "image_url": a.image_url,
    }
