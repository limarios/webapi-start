"""Dependências reutilizáveis dos endpoints da v1."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UnauthorizedError
from app.core.security import decode_token
from app.domain.user.entities import User, UserRole
from app.domain.user.services import UserService
from app.infrastructure.database.repositories.user import SqlAlchemyUserRepository
from app.infrastructure.database.session import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_user_service(session: SessionDep) -> UserService:
    """Constrói o UserService injetando o repositório SQLAlchemy."""
    repository = SqlAlchemyUserRepository(session)
    return UserService(repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: UserServiceDep,
) -> User:
    """Resolve o usuário autenticado a partir do JWT."""
    try:
        payload = decode_token(token)
    except UnauthorizedError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.message,
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    subject = payload.get("sub")
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sem subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    from uuid import UUID

    try:
        user_id = UUID(subject)
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Subject inválido no token",
        ) from exc

    user = await service._repo.get_by_id(user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inválido ou inativo",
        )
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def require_admin(current_user: CurrentUserDep) -> User:
    """Exige que o usuário autenticado seja admin."""
    if current_user.role is not UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão de administrador necessária",
        )
    return current_user


AdminDep = Annotated[User, Depends(require_admin)]
