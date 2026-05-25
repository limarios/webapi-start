"""Middlewares HTTP: secure headers e correlação de requests."""

from __future__ import annotations

import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class SecureHeadersMiddleware(BaseHTTPMiddleware):
    """Injeta cabeçalhos de segurança recomendados pela OWASP em toda resposta.

    Inclui CSP, COOP e CORP além dos cabeçalhos clássicos. A CSP é deliberadamente
    permissiva ('unsafe-inline' em style/script) para não quebrar Swagger UI/ReDoc;
    em produção, ajuste no `Content-Security-Policy` ou desabilite `/docs`.
    """

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        # Cabeçalhos clássicos
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault(
            "Strict-Transport-Security", "max-age=63072000; includeSubDomains"
        )
        response.headers.setdefault(
            "Permissions-Policy", "geolocation=(), microphone=(), camera=()"
        )
        response.headers.setdefault("X-XSS-Protection", "0")

        # CSP — restritiva mas compatível com Swagger UI/ReDoc.
        response.headers.setdefault(
            "Content-Security-Policy",
            (
                "default-src 'self'; "
                "img-src 'self' data: https://fastapi.tiangolo.com; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "font-src 'self' data:; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'"
            ),
        )

        # Cross-Origin isolation
        response.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        response.headers.setdefault("Cross-Origin-Resource-Policy", "same-site")

        return response


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Adiciona um X-Request-ID e mede a latência de cada requisição."""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start = time.perf_counter()

        response: Response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        response.headers["X-Request-ID"] = request_id
        logger.info(
            "%s %s -> %s (%.2fms) [request_id=%s]",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            request_id,
        )
        return response
