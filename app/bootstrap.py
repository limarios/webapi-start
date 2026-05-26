"""Script de bootstrap: cria o superusuário inicial se ele ainda não existir."""

from __future__ import annotations

import asyncio
import logging
import sys

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.domain.user.entities import UserRole
from app.domain.user.services import CreateUserInput, UserService
from app.infrastructure.database.repositories.user import SqlAlchemyUserRepository
from app.infrastructure.database.session import SessionLocal

logger = logging.getLogger(__name__)

_DEFAULT_PASSWORDS = {"Admin@123", "admin", "password"}


async def ensure_first_superuser() -> None:
    settings = get_settings()

    # Defesa em profundidade — apesar de o `Settings` já recusar a config em
    # produção, validamos novamente aqui caso o script seja chamado em modo
    # development apontando para um banco de produção por engano.
    if settings.is_production and settings.FIRST_SUPERUSER_PASSWORD in _DEFAULT_PASSWORDS:
        logger.error(
            "Bootstrap recusado: FIRST_SUPERUSER_PASSWORD está com valor padrão em "
            "ambiente de produção. Defina uma senha forte via variável de ambiente."
        )
        sys.exit(2)

    async with SessionLocal() as session:
        repo = SqlAlchemyUserRepository(session)
        service = UserService(repo)
        existing = await repo.get_by_email(settings.FIRST_SUPERUSER_EMAIL)
        if existing:
            logger.info("Superusuário já existe: %s", settings.FIRST_SUPERUSER_EMAIL)
            return
        await service.create(
            CreateUserInput(
                email=settings.FIRST_SUPERUSER_EMAIL,
                full_name="Administrador",
                password=settings.FIRST_SUPERUSER_PASSWORD,
                role=UserRole.ADMIN,
            )
        )
        logger.info("Superusuário criado: %s", settings.FIRST_SUPERUSER_EMAIL)


def main() -> None:
    configure_logging()
    asyncio.run(ensure_first_superuser())


if __name__ == "__main__":
    main()
