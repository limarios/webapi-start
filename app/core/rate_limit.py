"""Instância única do rate limiter usada pela aplicação.

Mantida em módulo separado para evitar import circular entre `app.main`
(que registra o middleware) e routers que querem aplicar limites por rota.
"""

from __future__ import annotations

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import get_settings


def _key_func(request) -> str:  # noqa: ANN001
    """Resolve o IP do cliente respeitando X-Forwarded-For.

    Quando a API está atrás de proxy (ex.: Cloud Run, ALB, Vercel),
    `get_remote_address` retorna o IP do proxy. Aqui priorizamos o
    primeiro IP do header X-Forwarded-For — o cliente original.
    """
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return get_remote_address(request)


_settings = get_settings()

limiter = Limiter(
    key_func=_key_func,
    default_limits=[f"{_settings.RATE_LIMIT_PER_MINUTE}/minute"],
    headers_enabled=True,
)
