"""Primitivas de segurança: hashing de senha e geração/validação de JWT."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext

from app.core.config import get_settings
from app.core.exceptions import UnauthorizedError

# argon2 é a recomendação atual da OWASP para hashing de senhas.
# bcrypt fica como fallback para hashes legados.
_password_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto",
)

# Hash dummy pré-computado usado para nivelar o tempo de verificação
# quando o usuário não existe (defesa contra user enumeration via timing).
_DUMMY_HASH = _password_context.hash("dummy-password-never-matches-any-real-user")


def hash_password(plain_password: str) -> str:
    """Gera um hash seguro (argon2id) para a senha em texto puro."""
    return _password_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se uma senha em texto puro corresponde ao hash armazenado."""
    return _password_context.verify(plain_password, hashed_password)


def consume_dummy_verify() -> None:
    """Executa um verify contra um hash dummy para nivelar timing.

    Use quando o usuário pesquisado não existe — o tempo gasto fica
    indistinguível do caminho onde o usuário existe e a senha está errada.
    """
    _password_context.verify("dummy-input", _DUMMY_HASH)


def create_access_token(
    subject: str | int,
    *,
    extra_claims: dict[str, Any] | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    """Gera um JWT de acesso assinado com a SECRET_KEY."""
    settings = get_settings()
    now = datetime.now(UTC)
    expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "access",
    }
    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """Valida e decodifica um JWT, levantando UnauthorizedError em caso de falha.

    Sempre passa um único algoritmo explícito para `decode`, fechando a porta
    de algorithm confusion: o token É forçado a usar o algoritmo configurado.
    """
    settings = get_settings()
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"require": ["exp", "iat", "sub"]},
        )
    except InvalidTokenError as exc:
        raise UnauthorizedError("Token inválido ou expirado") from exc
