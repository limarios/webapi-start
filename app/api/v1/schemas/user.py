"""Schemas Pydantic do recurso User."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr, Field

from app.domain.user.entities import UserRole

# ──────────────────────────────────────────────────────────────────────────────
# Validador de senha forte
# ──────────────────────────────────────────────────────────────────────────────

_COMMON_PASSWORDS = {
    "password", "12345678", "123456789", "1234567890", "qwerty12",
    "admin123", "admin@123", "password1", "letmein1", "welcome1",
    "iloveyou", "abc12345", "monkey12", "dragon12",
}

_HAS_LOWER = re.compile(r"[a-z]")
_HAS_UPPER = re.compile(r"[A-Z]")
_HAS_DIGIT = re.compile(r"\d")
_HAS_SYMBOL = re.compile(r"[^A-Za-z0-9]")


def _validate_strong_password(value: str) -> str:
    """Recusa senhas fracas. Regra: 12+ chars, com upper/lower/dígito/símbolo."""
    if len(value) < 12:
        raise ValueError("Senha precisa ter pelo menos 12 caracteres.")
    if not _HAS_LOWER.search(value):
        raise ValueError("Senha precisa ter pelo menos uma letra minúscula.")
    if not _HAS_UPPER.search(value):
        raise ValueError("Senha precisa ter pelo menos uma letra maiúscula.")
    if not _HAS_DIGIT.search(value):
        raise ValueError("Senha precisa ter pelo menos um dígito.")
    if not _HAS_SYMBOL.search(value):
        raise ValueError("Senha precisa ter pelo menos um símbolo.")
    if value.lower() in _COMMON_PASSWORDS:
        raise ValueError("Senha está em lista de senhas comuns.")
    return value


StrongPassword = Annotated[
    str,
    Field(min_length=12, max_length=128),
    AfterValidator(_validate_strong_password),
]


# ──────────────────────────────────────────────────────────────────────────────
# Schemas
# ──────────────────────────────────────────────────────────────────────────────


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)


class UserCreate(UserBase):
    password: StrongPassword
    role: UserRole = UserRole.USER


class AdminUserUpdate(BaseModel):
    """Update completo — somente admins têm acesso a esses campos."""

    full_name: str | None = Field(default=None, min_length=2, max_length=255)
    password: StrongPassword | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class SelfUserUpdate(BaseModel):
    """Update self-service — usuário comum pode editar somente seu próprio nome/senha.

    Note que NÃO existem campos `role` nem `is_active` aqui — é proposital
    para impedir privilege escalation por mass assignment.
    """

    full_name: str | None = Field(default=None, min_length=2, max_length=255)
    password: StrongPassword | None = None


# Alias retrocompatível — quem importava `UserUpdate` continua funcionando.
# Use `AdminUserUpdate` ou `SelfUserUpdate` em código novo.
UserUpdate = AdminUserUpdate


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
