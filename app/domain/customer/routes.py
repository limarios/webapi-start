from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customer.schemas import CustomerCreate, CustomerRead, CustomerUpdate
from app.domain.customer.service import CustomerService
from app.domain.customer.repository import CustomerRepository
from app.db.session import get_db

from app.api.v1.dependecies import get_current_user  # 🔒 Importando autenticação
from app.core.response import success_response, error_response  # ✅ Importando respostas padronizadas

router = APIRouter()

# Dependência para o CustomerService
async def get_customer_service(db: AsyncSession = Depends(get_db)) -> CustomerService:
    repo = CustomerRepository(db)
    return CustomerService(repo)

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Criar um novo cliente")
async def create_customer(
    customer: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
    current_user=Depends(get_current_user)  # 🔒 Exige autenticação
):
    """Cria um novo cliente no sistema."""
    customer_obj = await service.create_customer(customer)
    return success_response(data=customer_obj, message="Cliente criado com sucesso")

@router.get("/{customer_id}", response_model=dict, summary="Buscar dados do cliente pelo ID")
async def get_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service),
    current_user=Depends(get_current_user)  # 🔒 Exige autenticação
):
    """Obtém os detalhes de um cliente pelo ID."""
    customer = await service.get_customer(customer_id)
    if not customer:
        return error_response("Cliente não encontrado.")
    return success_response(data=customer, message="Cliente encontrado com sucesso")

@router.get("/", response_model=dict, summary="Listar todos os clientes")
async def list_customers(
    service: CustomerService = Depends(get_customer_service),
    current_user=Depends(get_current_user)  # 🔒 Exige autenticação
):
    """Lista todos os clientes cadastrados no sistema."""
    customers = await service.list_customers()
    if not customers:
        return error_response("Nenhum cliente encontrado.", details=[])
    return success_response(data=customers, message="Lista de clientes recuperada com sucesso")

@router.put("/{customer_id}", response_model=dict, summary="Atualizar dados do cliente")
async def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    service: CustomerService = Depends(get_customer_service),
    current_user=Depends(get_current_user)  # 🔒 Exige autenticação
):
    """Atualiza os dados de um cliente."""
    updated_customer = await service.update_customer(customer_id, customer_update)
    if not updated_customer:
        return error_response("Cliente não encontrado.")
    return success_response(data=updated_customer, message="Cliente atualizado com sucesso")

@router.delete("/{customer_id}", response_model=dict, summary="Deletar dados do cliente")
async def delete_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service),
    current_user=Depends(get_current_user)  # 🔒 Exige autenticação
):
    """Deleta um cliente do sistema."""
    success = await service.delete_customer(customer_id)
    if not success:
        return error_response("Cliente não encontrado.")
    return success_response(message="Cliente deletado com sucesso")
