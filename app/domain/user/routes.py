from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependecies import get_current_user
from app.db.session import get_db
from app.domain.user.repository import UserRepository
from app.domain.user.schemas import UserCreate, UserUpdate, UserRead
from app.domain.user.service import UserService
from app.core.response import success_response, error_response

router = APIRouter()

# Dependência para injetar o serviço no endpoint
async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)

@router.get("/me", response_model=dict, summary="Obter dados do usuário atual")
async def read_users_me(current_user=Depends(get_current_user)):
    """Retorna os dados do usuário autenticado."""
    user = await current_user  # Resolve a coroutine
    user_schema = UserRead.from_orm(user)  # Converte para Pydantic
    return success_response(data=user_schema)


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Criar um novo usuário")
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user)  # Protegido com JWT
):
    """Cria um novo usuário no sistema."""
    try:
        user = await service.create_user(user_data)
        return success_response(data=user, message="Usuário criado com sucesso")
    except ValueError as e:
        return error_response(str(e))

@router.get("/", response_model=dict, summary="Listar todos os usuários")
async def list_users(
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user)  # Protegido com JWT
):
    """Lista todos os usuários cadastrados no sistema."""
    users = await service.list_users()

    if not users:
        return error_response("Nenhum usuário encontrado.", details=[])

    return success_response(data=users, message="Lista de usuários recuperada com sucesso")

@router.get("/{user_id}", response_model=dict, summary="Buscar dados do usuário pelo ID")
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user)  # Protegido com JWT
):
    """Busca um usuário pelo ID."""
    user = await service.get_user(user_id)

    if not user:
        return error_response("Usuário não encontrado.", details={})

    return success_response(data=user, message="Usuário encontrado com sucesso")

@router.put("/{user_id}", response_model=dict, summary="Atualizar dados do usuário")
async def update_user(
    user_id: int,
    update_data: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user)  # Protegido com JWT
):
    """Atualiza os dados de um usuário."""
    try:
        user = await service.update_user(user_id, update_data)
        return success_response(data=user, message="Usuário atualizado com sucesso")
    except ValueError as e:
        return error_response(str(e))

@router.delete("/{user_id}", response_model=dict, summary="Deletar dados do usuário")
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user)  # Protegido com JWT
):
    """Deleta um usuário do sistema."""
    try:
        await service.delete_user(user_id)
        return success_response(message="Usuário deletado com sucesso")
    except ValueError as e:
        return error_response(str(e))
