"""Entidade de domínio User — independente de framework ou ORM."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4


class UserRole(StrEnum):
    """Papéis de usuário usados na autorização."""

    ADMIN = "admin"
    USER = "user"


@dataclass(slots=True)
class User:
    """Usuário do sistema.

    A entidade é construída sem dependências externas para ficar testável
    de forma isolada e desacoplada da camada de persistência.
    """

    email: str
    full_name: str
    hashed_password: str
    role: UserRole = UserRole.USER
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now())
    updated_at: datetime = field(default_factory=lambda: datetime.now())

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now()

    def promote(self) -> None:
        self.role = UserRole.ADMIN
        self.updated_at = datetime.now()

    @property
    def is_admin(self) -> bool:
        return self.role is UserRole.ADMIN
