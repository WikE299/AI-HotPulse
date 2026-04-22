from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.model_release import ModelRelease

router = APIRouter()


class ModelReleaseCreate(BaseModel):
    model_name: str
    organization: str
    version: Optional[str] = None
    release_date: str
    parameters_size: Optional[str] = None
    description: Optional[str] = None
    benchmarks: Optional[dict] = None
    announcement_url: Optional[str] = None
    category: str = "LLM"


@router.get("/model-releases")
async def list_model_releases(
    organization: Optional[str] = None,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(ModelRelease).order_by(asc(ModelRelease.release_date))
    if organization:
        stmt = stmt.where(ModelRelease.organization == organization)
    if category:
        stmt = stmt.where(ModelRelease.category == category)
    releases = (await db.scalars(stmt)).all()
    return [_serialize(r) for r in releases]


@router.post("/model-releases")
async def create_model_release(
    body: ModelReleaseCreate,
    db: AsyncSession = Depends(get_db),
):
    import uuid
    release = ModelRelease(
        id=str(uuid.uuid4()),
        model_name=body.model_name,
        organization=body.organization,
        version=body.version,
        release_date=body.release_date,
        parameters_size=body.parameters_size,
        description=body.description,
        benchmarks=body.benchmarks,
        announcement_url=body.announcement_url,
        category=body.category,
    )
    db.add(release)
    await db.commit()
    await db.refresh(release)
    return _serialize(release)


def _serialize(r: ModelRelease) -> dict:
    return {
        "id": r.id,
        "model_name": r.model_name,
        "organization": r.organization,
        "version": r.version,
        "release_date": r.release_date,
        "parameters_size": r.parameters_size,
        "description": r.description,
        "benchmarks": r.benchmarks or {},
        "announcement_url": r.announcement_url,
        "category": r.category,
    }
