"""Testes da camada de domínio (sem framework, sem DB real)."""

from __future__ import annotations

import pytest

from app.core.security import hash_password, verify_password
from app.domain.user.entities import User, UserRole


def test_user_defaults_to_role_user() -> None:
    user = User(
        email="x@y.z",
        full_name="X",
        hashed_password=hash_password("Secret@123"),
    )
    assert user.role is UserRole.USER
    assert user.is_active is True
    assert not user.is_admin


def test_user_promote() -> None:
    user = User(email="x@y.z", full_name="X", hashed_password="h")
    user.promote()
    assert user.is_admin


def test_user_deactivate() -> None:
    user = User(email="x@y.z", full_name="X", hashed_password="h")
    user.deactivate()
    assert user.is_active is False


def test_password_hashing_is_one_way() -> None:
    plain = "Strong@Password123"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed) is True
    assert verify_password("wrong", hashed) is False


@pytest.mark.parametrize("plain", ["a", "short"])
def test_password_hash_handles_any_length(plain: str) -> None:
    # A regra de tamanho mínimo é de schema (Pydantic), não do hashing.
    assert verify_password(plain, hash_password(plain))
