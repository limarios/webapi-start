"""Casos de uso (application services) do domínio de usuários."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from app.core.security import consume_dummy_verify, hash_password, verify_password
from app.domain.user.entities import User, UserRole
from app.domain.user.exceptions import (
    EmailAlreadyRegisteredError,
    InactiveUserError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from app.domain.user.repository import UserRepository


@dataclass(slots=True)
class CreateUserInput:
    email: str
    full_name: str
    password: str
    role: UserRole = UserRole.USER


@dataclass(slots=True)
class UpdateUserInput:
    full_name: str | None = None
    password: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserService:
    """Orquestra regras de negócio em torno do agregado User."""

    def __init__(self, repository: UserRepository) -> None:
        self._repo = repository

    async def create(self, data: CreateUserInput) -> User:
        if await self._repo.get_by_email(data.email):
            raise EmailAlreadyRegisteredError()

        user = User(
            email=data.email.lower().strip(),
            full_name=data.full_name.strip(),
            hashed_password=hash_password(data.password),
            role=data.role,
        )
        return await self._repo.add(user)

    async def get(self, user_id: UUID) -> User:
        user = await self._repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user

    async def list(self, *, skip: int = 0, limit: int = 100) -> list[User]:
        return await self._repo.list_all(skip=skip, limit=limit)

    async def update(self, user_id: UUID, data: UpdateUserInput) -> User:
        user = await self.get(user_id)

        if data.full_name is not None:
            user.full_name = data.full_name.strip()
        if data.password is not None:
            user.hashed_password = hash_password(data.password)
        if data.role is not None:
            user.role = data.role
        if data.is_active is not None:
            user.is_active = data.is_active

        return await self._repo.update(user)

    async def delete(self, user_id: UUID) -> None:
        await self.get(user_id)
        await self._repo.delete(user_id)

    async def authenticate(self, email: str, password: str) -> User:
        user = await self._repo.get_by_email(email.lower().strip())
        # Defesa contra user enumeration por timing: quando o usuário não
        # existe, ainda assim consumimos um Argon2 verify dummy para que o
        # tempo de resposta seja indistinguível do caminho "senha errada".
        if not user:
            consume_dummy_verify()
            raise InvalidCredentialsError()
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
        if not user.is_active:
            raise InactiveUserError()
        return user
