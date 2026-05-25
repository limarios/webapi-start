"""Endpoints de saúde e prontidão da aplicação."""

from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import text

from app.api.v1.dependencies import SessionDep
from app.api.v1.schemas.common import HealthResponse
from app.core.config import get_settings

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse, summary="Health check da API")
async def health_check(session: SessionDep) -> HealthResponse:
    settings = get_settings()
    try:
        result = await session.execute(text("SELECT 1"))
        db_status = "connected" if result.scalar() == 1 else "disconnected"
    except Exception:
        db_status = "disconnected"

    return HealthResponse(
        status="ok" if db_status == "connected" else "degraded",
        database=db_status,
        version=settings.APP_VERSION,
    )


@router.get("/health/live", summary="Liveness probe")
async def liveness() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/health/ready", summary="Readiness probe")
async def readiness(session: SessionDep) -> dict[str, str]:
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        return {"status": "not_ready"}
