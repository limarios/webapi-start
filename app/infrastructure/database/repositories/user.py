"""Implementação concreta do UserRepository usando SQLAlchemy assíncrono."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.entities import User, UserRole
from app.infrastructure.database.models.user import UserModel


def _to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        email=model.email,
        full_name=model.full_name,
        hashed_password=model.hashed_password,
        role=UserRole(model.role),
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _apply_entity(model: UserModel, entity: User) -> None:
    model.email = entity.email
    model.full_name = entity.full_name
    model.hashed_password = entity.hashed_password
    model.role = entity.role.value
    model.is_active = entity.is_active


class SqlAlchemyUserRepository:
    """Adapter do `UserRepository` para SQLAlchemy + Postgres."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, user: User) -> User:
        model = UserModel(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            hashed_password=user.hashed_password,
            role=user.role.value,
            is_active=user.is_active,
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return _to_entity(model)

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email.lower())
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list_all(self, *, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self._session.execute(
            select(UserModel).order_by(UserModel.created_at.desc()).offset(skip).limit(limit)
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def update(self, user: User) -> User:
        result = await self._session.execute(select(UserModel).where(UserModel.id == user.id))
        model = result.scalar_one()
        _apply_entity(model, user)
        await self._session.commit()
        await self._session.refresh(model)
        return _to_entity(model)

    async def delete(self, user_id: UUID) -> None:
        result = await self._session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.commit()
