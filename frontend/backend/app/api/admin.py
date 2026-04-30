from fastapi import APIRouter

router = APIRouter()


@router.post("/crawl/trigger")
async def trigger_crawl():
    import asyncio
    from app.pipeline import run_crawl_pipeline
    asyncio.create_task(run_crawl_pipeline())
    return {"message": "Crawl started in background"}
