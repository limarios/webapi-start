from typing import List, Optional
from app.domain.customer.repository import CustomerRepository
from app.domain.customer.schemas import CustomerCreate, CustomerRead, CustomerUpdate


class CustomerService:
    def __init__(self, repo: CustomerRepository):
        self.repo = repo

    async def create_customer(self, customer_data: CustomerCreate) -> CustomerRead:
        customer = await self.repo.create_customer(customer_data)
        return CustomerRead.from_orm(customer)

    async def get_customer(self, customer_id: int) -> Optional[CustomerRead]:
        customer = await self.repo.get_customer_by_id(customer_id)
        return CustomerRead.from_orm(customer) if customer else None

    async def list_customers(self) -> List[CustomerRead]:
        customers = await self.repo.list_customers()
        return [CustomerRead.from_orm(c) for c in customers]

    async def update_customer(self, customer_id: int, update_data: CustomerUpdate) -> Optional[CustomerRead]:
        customer = await self.repo.get_customer_by_id(customer_id)
        if not customer:
            return None
        updated_customer = await self.repo.update_customer(customer, update_data)
        return CustomerRead.from_orm(updated_customer)

    async def delete_customer(self, customer_id: int) -> bool:
        customer = await self.repo.get_customer_by_id(customer_id)
        if not customer:
            return False
        await self.repo.delete_customer(customer)
        return True
