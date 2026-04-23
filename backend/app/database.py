from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text

from app.config import settings

engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    # Import all models so they register with Base.metadata
    from app.models import article, topic, brief, model_release, prediction  # noqa

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _migrate(conn)
        from app.seed_model_releases import seed_model_releases
        await seed_model_releases(conn)
        from app.seed_predictions import seed_predictions
        await seed_predictions(conn)


async def _migrate(conn):
    new_cols = [
        ("articles", "paper_contribution", "TEXT"),
        ("articles", "readability_score", "INTEGER"),
        ("articles", "topic_id",          "TEXT"),
    ]
    for table, col, col_type in new_cols:
        try:
            await conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}"))
        except Exception:
            pass  # Column already exists

