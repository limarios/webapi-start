"""Fixtures globais da suíte de testes.

Os testes rodam contra um SQLite em memória, sem dependência de Docker.
A app é exercitada via `httpx.AsyncClient + ASGITransport`, ou seja, sem
abrir socket de rede.
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator

# Settings de teste devem ser definidas ANTES de importar `app.*`.
os.environ.setdefault("APP_ENV", "testing")
os.environ.setdefault("APP_DEBUG", "true")
os.environ.setdefault(
    "SECRET_KEY",
    "test-only-secret-key-do-not-use-in-production-1234567890abcdef",
)
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("RATE_LIMIT_PER_MINUTE", "1000")

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.v1.dependencies import get_user_service
from app.core.security import hash_password
from app.domain.user.entities import UserRole
from app.domain.user.services import UserService
from app.infrastructure.database.base import Base
from app.infrastructure.database.models.user import UserModel
from app.infrastructure.database.repositories.user import SqlAlchemyUserRepository
from app.infrastructure.database.session import get_session
from app.main import app


@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine) -> AsyncIterator[AsyncSession]:
    session_maker = async_sessionmaker(db_engine, expire_on_commit=False)
    async with session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session) -> AsyncIterator[AsyncClient]:
    async def override_get_session():
        yield db_session

    async def override_user_service():
        return UserService(SqlAlchemyUserRepository(db_session))

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_user_service] = override_user_service

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def admin_user(db_session) -> UserModel:
    user = UserModel(
        email="admin@test.local",
        full_name="Admin Test",
        hashed_password=hash_password("Admin@123"),
        role=UserRole.ADMIN.value,
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def regular_user(db_session) -> UserModel:
    user = UserModel(
        email="user@test.local",
        full_name="Regular User",
        hashed_password=hash_password("User@1234"),
        role=UserRole.USER.value,
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def admin_token(client: AsyncClient, admin_user) -> str:
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": admin_user.email, "password": "Admin@123"},
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def auth_headers(admin_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {admin_token}"}
