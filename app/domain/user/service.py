from app.domain.user.repository import UserRepository
from app.domain.user.schemas import UserCreate, UserUpdate, UserRead
from app.infra.logger import logger


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, user_data: UserCreate) -> UserRead:
        """Cria um novo usuário, verificando se o e-mail já existe."""
        existing = await self.repo.get_user_by_email(user_data.email)
        if existing:
            raise ValueError("Email já está em uso.")

        logger.info(f"Criando novo usuário: {user_data.email}")
        user = await self.repo.create_user(user_data)
        logger.info(f"Usuário criado com sucesso! ID: {user.id}")
        return UserRead.from_orm(user)

    async def get_user(self, user_id: int) -> UserRead | None:
        """Busca um usuário pelo ID."""
        user = await self.repo.get_user_by_id(user_id)
        return UserRead.from_orm(user) if user else None

    async def update_user(self, user_id: int, update_data: UserUpdate) -> UserRead:
        """Atualiza os dados de um usuário."""
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        updated_user = await self.repo.update_user(user, update_data)
        return UserRead.from_orm(updated_user)

    async def delete_user(self, user_id: int):
        """Exclui um usuário do sistema."""
        logger.info(f"Buscando usuário para exclusão: {user_id}")
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        await self.repo.delete_user(user)
        logger.info(f"Usuário {user.nome} removido com sucesso.")

    async def list_users(self) -> list[UserRead]:
        """Retorna a lista de usuários cadastrados."""
        users = await self.repo.list_users()
        return [UserRead.from_orm(u) for u in users]

    async def get_user_by_username(self, username: str):
        """Busca um usuário pelo login."""
        logger.info(f"Buscando usuário: {username}")
        user = await self.repo.get_user_by_username(username)
        if user:
            logger.info(f"Usuário encontrado: {user.nome}")
        else:
            logger.warning(f"Usuário {username} não encontrado")
        return user
