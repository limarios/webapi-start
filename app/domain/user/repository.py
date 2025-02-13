from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.user.models import User  # Importe o modelo, não os schemas
from app.domain.user.schemas import UserUpdate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data) -> User:
        """Cria um novo usuário no banco de dados."""
        user = User(
            nome=user_data.nome,
            email=user_data.email,
            senha=user_data.senha,
            login=user_data.login,
            grupo=user_data.grupo,
            telefone=user_data.telefone,
            cargo=user_data.cargo,
            setor=user_data.setor,
            ativo=user_data.ativo
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Obtém um usuário pelo ID."""
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        """Obtém um usuário pelo e-mail."""
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def update_user(self, db_user: User, update_data: UserUpdate) -> User:
        """Atualiza os dados de um usuário."""
        update_dict = update_data.dict(exclude_unset=True)  # Apenas campos enviados
        for field, value in update_dict.items():
            setattr(db_user, field, value)

        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def delete_user(self, db_user: User):
        """Remove um usuário do banco de dados."""
        await self.db.delete(db_user)
        await self.db.commit()

    async def list_users(self) -> list[User]:
        """Retorna a lista de usuários cadastrados."""
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_user_by_username(self, username: str) -> User | None:
        """Busca um usuário pelo login."""
        result = await self.db.execute(select(User).filter(User.login == username))
        return result.scalars().first()
