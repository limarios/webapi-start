"""Endpoints de autenticação."""

from __future__ import annotations

from fastapi import APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.dependencies import UserServiceDep
from app.api.v1.schemas.auth import TokenResponse
from app.core.config import get_settings
from app.core.security import create_access_token
from typing import Annotated

from fastapi import Depends

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Autentica usuário e devolve JWT de acesso",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDep,
) -> TokenResponse:
    """Login compatível com o fluxo OAuth2 password do Swagger.

    O campo `username` do formulário deve receber o e-mail do usuário.
    """
    user = await service.authenticate(form_data.username, form_data.password)
    settings = get_settings()
    access_token = create_access_token(
        subject=user.id,
        extra_claims={"role": user.role.value, "email": user.email},
    )
    return TokenResponse(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
