"""Configuração da aplicação carregada do ambiente via Pydantic Settings."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal
from urllib.parse import urlparse

from pydantic import Field, PostgresDsn, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

JwtAlgorithm = Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512", "ES256", "ES384"]


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
    APP_VERSION: str = "1.1.0"

    # Banco
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_DB: str = "webapi_start"
    DATABASE_URL: PostgresDsn | None = None
    POSTGRES_SSL_REQUIRED: bool = False  # auto-ativado quando APP_ENV=production

    # Segurança
    SECRET_KEY: str = Field(min_length=32)
    JWT_ALGORITHM: JwtAlgorithm = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15, ge=1, le=60)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24 * 7, ge=60)

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    # Rate limit
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, ge=1)
    LOGIN_RATE_LIMIT_PER_MINUTE: int = Field(default=5, ge=1)

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_JSON: bool = False

    # Bootstrap
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = Field(default="Admin@123", min_length=8)

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

    @model_validator(mode="after")
    def enforce_production_safety(self) -> "Settings":
        """Validações que só fazem sentido quando APP_ENV=production."""
        if self.APP_ENV != "production":
            return self

        # CORS não pode conter wildcard com credentials.
        if "*" in self.CORS_ORIGINS:
            raise ValueError(
                "CORS_ORIGINS não pode conter '*' em produção (allow_credentials=True)."
            )

        # Todas as origens devem usar HTTPS em produção.
        for origin in self.cors_origins_list:
            parsed = urlparse(origin)
            if parsed.scheme != "https":
                raise ValueError(
                    f"CORS_ORIGINS em produção exige HTTPS — origem inválida: {origin!r}"
                )

        # DATABASE_URL precisa exigir SSL em produção.
        url = str(self.DATABASE_URL or "")
        if "sslmode=" not in url and "ssl=" not in url:
            # Auto-injetar sslmode=require para asyncpg
            sep = "&" if "?" in url else "?"
            object.__setattr__(self, "DATABASE_URL", f"{url}{sep}ssl=require")
        self.POSTGRES_SSL_REQUIRED = True

        # Bloquear senha padrão de superusuário em produção.
        if self.FIRST_SUPERUSER_PASSWORD in {"Admin@123", "admin", "password"}:
            raise ValueError(
                "FIRST_SUPERUSER_PASSWORD não pode usar o valor padrão em produção. "
                "Defina uma senha forte via variável de ambiente."
            )

        # SECRET_KEY de exemplo é proibida em produção.
        if "change-me" in self.SECRET_KEY.lower() or "test" in self.SECRET_KEY.lower():
            raise ValueError(
                "SECRET_KEY parece ser um valor de exemplo. "
                "Gere uma chave forte com secrets.token_urlsafe(64)."
            )

        return self

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
