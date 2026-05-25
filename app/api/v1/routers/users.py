"""Endpoints CRUD do recurso User."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Query, status

from app.api.v1.dependencies import AdminDep, CurrentUserDep, UserServiceDep
from app.api.v1.schemas.user import UserCreate, UserRead, UserUpdate
from app.domain.user.services import CreateUserInput, UpdateUserInput

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead, summary="Retorna o usuário autenticado")
async def me(current_user: CurrentUserDep) -> UserRead:
    return UserRead.model_validate(current_user)


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um usuário (requer admin)",
)
async def create_user(
    payload: UserCreate,
    service: UserServiceDep,
    _: AdminDep,
) -> UserRead:
    user = await service.create(
        CreateUserInput(
            email=payload.email,
            full_name=payload.full_name,
            password=payload.password,
            role=payload.role,
        )
    )
    return UserRead.model_validate(user)


@router.get(
    "/",
    response_model=list[UserRead],
    summary="Lista usuários (requer admin)",
)
async def list_users(
    service: UserServiceDep,
    _: AdminDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[UserRead]:
    users = await service.list(skip=skip, limit=limit)
    return [UserRead.model_validate(u) for u in users]


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Detalhe de um usuário (requer admin)",
)
async def get_user(
    user_id: UUID,
    service: UserServiceDep,
    _: AdminDep,
) -> UserRead:
    user = await service.get(user_id)
    return UserRead.model_validate(user)


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    summary="Atualiza um usuário (requer admin)",
)
async def update_user(
    user_id: UUID,
    payload: UserUpdate,
    service: UserServiceDep,
    _: AdminDep,
) -> UserRead:
    user = await service.update(
        user_id,
        UpdateUserInput(
            full_name=payload.full_name,
            password=payload.password,
            role=payload.role,
            is_active=payload.is_active,
        ),
    )
    return UserRead.model_validate(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um usuário (requer admin)",
)
async def delete_user(
    user_id: UUID,
    service: UserServiceDep,
    _: AdminDep,
) -> None:
    await service.delete(user_id)
