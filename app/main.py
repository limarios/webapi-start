"""Entry-point da aplicação FastAPI."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.error_handlers import register_exception_handlers
from app.api.middleware import RequestContextMiddleware, SecureHeadersMiddleware
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.rate_limit import limiter

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    yield


def create_app() -> FastAPI:
    """Application factory — facilita testes e múltiplas instâncias."""
    app = FastAPI(
        title=settings.APP_NAME,
        description=(
            "API base profissional construída com FastAPI seguindo Clean Architecture e "
            "Domain-Driven Design. Pronta para ser usada como ponto de partida para "
            "projetos reais — segura, testada e observável."
        ),
        version=settings.APP_VERSION,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
        contact={
            "name": "Matheus de Lima Rios",
            "email": "limariosprofissional@gmail.com",
        },
        license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    )

    # Rate limiting (instância compartilhada com routers que aplicam @limiter.limit)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    )

    # Cabeçalhos de segurança e correlação de requests
    app.add_middleware(SecureHeadersMiddleware)
    app.add_middleware(RequestContextMiddleware)

    # Handlers de erro consistentes
    register_exception_handlers(app)

    # Rotas da v1
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/", tags=["Root"], include_in_schema=False)
    async def root() -> dict[str, str]:
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
            "docs": "/docs" if not settings.is_production else "disabled",
        }

    return app


app = create_app()
