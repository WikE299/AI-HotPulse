import hashlib
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.prediction import Prediction

router = APIRouter()


@router.get("/predictions/today")
async def today_prediction(db: AsyncSession = Depends(get_db)):
    total = await db.scalar(select(func.count()).select_from(Prediction))
    if not total:
        return None
    today_str = date.today().isoformat()
    idx = int(hashlib.md5(today_str.encode()).hexdigest(), 16) % total
    stmt = select(Prediction).offset(idx).limit(1)
    pred = await db.scalar(stmt)
    return _serialize(pred) if pred else None


@router.get("/predictions")
async def list_predictions(db: AsyncSession = Depends(get_db)):
    stmt = select(Prediction).order_by(Prediction.person_name)
    results = (await db.scalars(stmt)).all()
    return [_serialize(p) for p in results]


def _serialize(p: Prediction) -> dict:
    return {
        "id": p.id,
        "person_name": p.person_name,
        "person_title": p.person_title,
        "person_org": p.person_org,
        "avatar_file": p.avatar_file,
        "quote": p.quote,
        "quote_source": p.quote_source,
        "quote_date": p.quote_date,
        "deadline": p.deadline,
        "category": p.category,
        "status": p.status,
        "credibility_note": p.credibility_note,
    }
