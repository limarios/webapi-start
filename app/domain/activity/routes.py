from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.activity.schemas import ActivityCreate, ActivityRead, ActivityUpdate
from app.domain.activity.service import ActivityService
from app.domain.activity.repository import ActivityRepository
from app.db.session import get_db

from app.api.v1.dependecies import get_current_user  # 🔒 Importando autenticação
from app.core.response import success_response, error_response  # ✅ Importando respostas padronizadas

router = APIRouter()

# Dependência para o ActivityService
async def get_activity_service(db: AsyncSession = Depends(get_db)) -> ActivityService:
    repo = ActivityRepository(db)
    return ActivityService(repo)

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity: ActivityCreate,
    service: ActivityService = Depends(get_activity_service),
    current_user=Depends(get_current_user)  # 🔒 Exige autenticação
):
    """Cria uma nova atividade no sistema."""
    activity_obj = await service.create_activity(activity)
    return success_response(data=activity_obj, message="Atividade criada com sucesso")

@router.get("/{activity_id}", response_model=dict)
async def get_activity(
    activity_id: int,
    service: ActivityService = Depends(get_activity_service),
    current_user=Depends(get_current_user)  # 🔒 Exige autenticação
):
    """Obtém os detalhes de uma atividade pelo ID."""
    activity = await service.get_activity(activity_id)
    if not activity:
        return error_response("Atividade não encontrada.")
    return success_response(data=activity, message="Atividade encontrada com sucesso")

@router.get("/", response_model=dict)
async def list_activities(
    service: ActivityService = Depends(get_activity_service),
    current_user=Depends(get_current_user)  # 🔒 Exige autenticação
):
    """Lista todas as atividades cadastradas no sistema."""
    activities = await service.list_activities()
    if not activities:
        return error_response("Nenhuma atividade encontrada.", details=[])
    return success_response(data=activities, message="Lista de atividades recuperada com sucesso")

@router.put("/{activity_id}", response_model=dict)
async def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    service: ActivityService = Depends(get_activity_service),
    current_user=Depends(get_current_user)  # 🔒 Exige autenticação
):
    """Atualiza os dados de uma atividade."""
    updated_activity = await service.update_activity(activity_id, activity_update)
    if not updated_activity:
        return error_response("Atividade não encontrada.")
    return success_response(data=updated_activity, message="Atividade atualizada com sucesso")

@router.delete("/{activity_id}", response_model=dict)
async def delete_activity(
    activity_id: int,
    service: ActivityService = Depends(get_activity_service),
    current_user=Depends(get_current_user)  # 🔒 Exige autenticação
):
    """Deleta uma atividade do sistema."""
    success = await service.delete_activity(activity_id)
    if not success:
        return error_response("Atividade não encontrada.")
    return success_response(message="Atividade deletada com sucesso")
