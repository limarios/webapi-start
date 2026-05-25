"""Contrato (interface) do repositório de usuários.

A implementação concreta vive em `app/infrastructure/database/repositories/`
para respeitar a regra da dependência de Clean Architecture.
"""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from app.domain.user.entities import User


class UserRepository(Protocol):
    async def add(self, user: User) -> User: ...

    async def get_by_id(self, user_id: UUID) -> User | None: ...

    async def get_by_email(self, email: str) -> User | None: ...

    async def list_all(self, *, skip: int = 0, limit: int = 100) -> list[User]: ...

    async def update(self, user: User) -> User: ...

    async def delete(self, user_id: UUID) -> None: ...
