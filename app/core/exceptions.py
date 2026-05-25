"""Exceções base da aplicação (independentes de framework)."""

from __future__ import annotations


class AppError(Exception):
    """Erro base da aplicação. Subclasses representam condições semânticas específicas."""

    status_code: int = 500
    code: str = "internal_error"
    message: str = "Erro interno na aplicação"

    def __init__(self, message: str | None = None, *, code: str | None = None) -> None:
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        super().__init__(self.message)


class NotFoundError(AppError):
    status_code = 404
    code = "not_found"
    message = "Recurso não encontrado"


class ConflictError(AppError):
    status_code = 409
    code = "conflict"
    message = "Conflito ao processar o recurso"


class ValidationAppError(AppError):
    status_code = 422
    code = "validation_error"
    message = "Dados inválidos"


class UnauthorizedError(AppError):
    status_code = 401
    code = "unauthorized"
    message = "Credenciais inválidas ou ausentes"


class ForbiddenError(AppError):
    status_code = 403
    code = "forbidden"
    message = "Acesso negado"
