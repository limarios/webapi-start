"""Endpoints de autenticação."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.dependencies import UserServiceDep
from app.api.v1.schemas.auth import TokenResponse
from app.core.config import get_settings
from app.core.rate_limit import limiter
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])
_settings = get_settings()


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Autentica usuário e devolve JWT de acesso",
)
@limiter.limit(f"{_settings.LOGIN_RATE_LIMIT_PER_MINUTE}/minute")
async def login(
    request: Request,  # noqa: ARG001 — exigido pelo SlowAPI para rate limit
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDep,
) -> TokenResponse:
    """Login compatível com o fluxo OAuth2 password do Swagger.

    O campo `username` do formulário deve receber o e-mail do usuário.
    Rate limit dedicado é aplicado (default 5 tentativas/minuto/IP).
    """
    user = await service.authenticate(form_data.username, form_data.password)
    access_token = create_access_token(
        subject=user.id,
        # Apenas `role` no JWT — `email` e demais PII vêm via /users/me sob auth.
        extra_claims={"role": user.role.value},
    )
    return TokenResponse(
        access_token=access_token,
        expires_in=_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
