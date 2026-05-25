"""Testes do CRUD de usuários."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user_requires_admin(
    client: AsyncClient, regular_user
) -> None:
    # Login como usuário comum
    login = await client.post(
        "/api/v1/auth/login",
        data={"username": regular_user.email, "password": "User@1234"},
    )
    token = login.json()["access_token"]

    response = await client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "new@example.com",
            "full_name": "New User",
            "password": "Strong@123",
        },
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_can_create_user(client: AsyncClient, auth_headers) -> None:
    response = await client.post(
        "/api/v1/users/",
        headers=auth_headers,
        json={
            "email": "new@example.com",
            "full_name": "New User",
            "password": "Strong@123",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "new@example.com"
    assert body["role"] == "user"
    assert "id" in body


@pytest.mark.asyncio
async def test_cannot_create_duplicate_email(client: AsyncClient, auth_headers) -> None:
    payload = {
        "email": "dup@example.com",
        "full_name": "Dup",
        "password": "Strong@123",
    }
    first = await client.post("/api/v1/users/", headers=auth_headers, json=payload)
    assert first.status_code == 201

    second = await client.post("/api/v1/users/", headers=auth_headers, json=payload)
    assert second.status_code == 409
    assert second.json()["code"] == "email_already_registered"


@pytest.mark.asyncio
async def test_list_users(client: AsyncClient, auth_headers, admin_user) -> None:
    response = await client.get("/api/v1/users/", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert any(u["email"] == admin_user.email for u in body)


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, auth_headers) -> None:
    created = await client.post(
        "/api/v1/users/",
        headers=auth_headers,
        json={
            "email": "to-update@example.com",
            "full_name": "Old Name",
            "password": "Strong@123",
        },
    )
    user_id = created.json()["id"]

    response = await client.patch(
        f"/api/v1/users/{user_id}",
        headers=auth_headers,
        json={"full_name": "New Name"},
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "New Name"


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, auth_headers) -> None:
    created = await client.post(
        "/api/v1/users/",
        headers=auth_headers,
        json={
            "email": "to-delete@example.com",
            "full_name": "Bye",
            "password": "Strong@123",
        },
    )
    user_id = created.json()["id"]

    response = await client.delete(f"/api/v1/users/{user_id}", headers=auth_headers)
    assert response.status_code == 204

    follow_up = await client.get(f"/api/v1/users/{user_id}", headers=auth_headers)
    assert follow_up.status_code == 404
