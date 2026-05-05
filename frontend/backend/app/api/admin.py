from fastapi import APIRouter

router = APIRouter()


@router.post("/crawl/trigger")
async def trigger_crawl():
    from app.pipeline import run_crawl_pipeline
    count = await run_crawl_pipeline()
    return {"message": f"Crawl completed, {count} articles added"}
