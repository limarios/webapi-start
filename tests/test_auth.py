"""Testes do fluxo de autenticação."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_with_valid_credentials(client: AsyncClient, admin_user) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": admin_user.email, "password": "Admin@Pass123!"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["expires_in"] > 0


@pytest.mark.asyncio
async def test_login_with_invalid_password(client: AsyncClient, admin_user) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": admin_user.email, "password": "WrongPassword"},
    )
    assert response.status_code == 401
    assert response.json()["code"] == "invalid_credentials"


@pytest.mark.asyncio
async def test_login_with_unknown_email(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "ghost@nowhere.tld", "password": "AnyPass1!"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_returns_authenticated_user(
    client: AsyncClient, admin_user, auth_headers
) -> None:
    response = await client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == admin_user.email
    assert body["role"] == "admin"
