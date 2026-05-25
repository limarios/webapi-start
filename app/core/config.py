"""Configuração da aplicação carregada do ambiente via Pydantic Settings."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings da API. Lê variáveis do ambiente e do arquivo .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Aplicação
    APP_NAME: str = "WebAPI Start"
    APP_ENV: Literal["development", "testing", "production"] = "development"
    APP_DEBUG: bool = False
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_VERSION: str = "1.0.0"

    # Banco
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_DB: str = "webapi_start"
    DATABASE_URL: PostgresDsn | None = None

    # Segurança
    SECRET_KEY: str = Field(min_length=32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    # Rate limit
    RATE_LIMIT_PER_MINUTE: int = 60

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_JSON: bool = False

    # Bootstrap
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "Admin@123"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_database_url(cls, v: str | None, info) -> str:
        if isinstance(v, str) and v:
            return v
        data = info.data
        return (
            f"postgresql+asyncpg://{data.get('POSTGRES_USER')}:{data.get('POSTGRES_PASSWORD')}"
            f"@{data.get('POSTGRES_HOST')}:{data.get('POSTGRES_PORT')}/{data.get('POSTGRES_DB')}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def sync_database_url(self) -> str:
        """URL síncrona usada por Alembic."""
        return str(self.DATABASE_URL).replace("postgresql+asyncpg", "postgresql+psycopg2")


@lru_cache
def get_settings() -> Settings:
    """Retorna as configurações em cache (instância única)."""
    return Settings()  # type: ignore[call-arg]
