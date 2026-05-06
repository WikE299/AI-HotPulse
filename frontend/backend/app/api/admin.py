from fastapi import APIRouter, HTTPException

from app.config import settings

router = APIRouter()


@router.post("/crawl/trigger")
async def trigger_crawl():
    if not settings.allow_manual_crawl:
        raise HTTPException(status_code=409, detail="Manual crawl is disabled on this deployment")
    from app.pipeline import run_crawl_pipeline
    count = await run_crawl_pipeline()
    return {"message": f"Crawl completed, {count} articles added"}


@router.get("/crawl/trigger")
async def trigger_crawl_cron():
    from app.pipeline import run_crawl_pipeline
    count = await run_crawl_pipeline()
    return {"message": f"Crawl completed, {count} articles added"}
