"""Engine e sessão assíncrona do SQLAlchemy."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

_settings = get_settings()
_database_url = str(_settings.DATABASE_URL)

_engine_kwargs: dict[str, Any] = {"echo": False, "future": True, "pool_pre_ping": True}
if not _database_url.startswith("sqlite"):
    # SQLite (usado nos testes, em memória) usa StaticPool e rejeita
    # pool_size/max_overflow — só fazem sentido para QueuePool (Postgres).
    _engine_kwargs.update(pool_size=10, max_overflow=20)

engine = create_async_engine(_database_url, **_engine_kwargs)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Dependency do FastAPI: cria e fecha uma sessão assíncrona por request."""
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
