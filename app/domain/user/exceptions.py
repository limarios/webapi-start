"""Exceções específicas do domínio de usuário."""

from __future__ import annotations

from app.core.exceptions import ConflictError, NotFoundError, UnauthorizedError


class UserNotFoundError(NotFoundError):
    code = "user_not_found"
    message = "Usuário não encontrado"


class EmailAlreadyRegisteredError(ConflictError):
    code = "email_already_registered"
    message = "E-mail já cadastrado"


class InvalidCredentialsError(UnauthorizedError):
    code = "invalid_credentials"
    message = "Credenciais inválidas"


class InactiveUserError(UnauthorizedError):
    code = "inactive_user"
    message = "Usuário inativo"
