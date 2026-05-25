"""Schemas Pydantic genéricos reutilizáveis."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    code: str = Field(..., description="Código identificador do erro")
    message: str = Field(..., description="Descrição legível do erro")
    details: dict[str, Any] | list[Any] | None = None


class HealthResponse(BaseModel):
    status: str = Field(..., examples=["ok"])
    database: str = Field(..., examples=["connected"])
    version: str
