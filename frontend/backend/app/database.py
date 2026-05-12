from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text

import ssl as _ssl
from app.config import settings

_db_url = settings.database_url
if _db_url.startswith("postgresql://"):
    _db_url = _db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# asyncpg uses `ssl` param, not `sslmode`; also strip channel_binding
_connect_args = {}
if "sslmode=" in _db_url or "channel_binding=" in _db_url:
    import urllib.parse
    parsed = urllib.parse.urlparse(_db_url)
    qs = urllib.parse.parse_qs(parsed.query)
    sslmode = (qs.pop("sslmode", [None]) or [None])[0]
    qs.pop("channel_binding", None)
    new_query = urllib.parse.urlencode(qs, doseq=True)
    _db_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
    if sslmode in ("require", "verify-ca", "verify-full"):
        ctx = _ssl.create_default_context()
        if sslmode in ("verify-ca", "verify-full"):
            ctx.check_hostname = True
            ctx.verify_mode = _ssl.CERT_REQUIRED
        else:
            ctx.check_hostname = False
            ctx.verify_mode = _ssl.CERT_NONE
        _connect_args["ssl"] = ctx

_connect_args.setdefault("timeout", 5)
_connect_args.setdefault("command_timeout", 5)
_engine_kwargs = {
    "echo": False,
    "pool_pre_ping": True,
    "connect_args": _connect_args,
}
if _db_url.startswith("postgresql"):
    _engine_kwargs.update(pool_size=5, max_overflow=5)

engine = create_async_engine(_db_url, **_engine_kwargs)
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
        ("articles", "recommend_reason",  "TEXT"),
    ]
    for table, col, col_type in new_cols:
        try:
            async with conn.begin_nested():
                await conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}"))
        except Exception:
            pass  # Column already exists or backend doesn't support the alteration
