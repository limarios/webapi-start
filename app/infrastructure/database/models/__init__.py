"""Modelos ORM. Importados aqui para o Alembic detectá-los via metadata."""

from app.infrastructure.database.models.user import UserModel

__all__ = ["UserModel"]
