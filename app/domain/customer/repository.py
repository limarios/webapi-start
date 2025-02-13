from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.domain.customer.models import Customer
from app.domain.customer.schemas import CustomerCreate, CustomerUpdate

class CustomerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_customer(self, customer_data: CustomerCreate) -> Customer:
        customer = Customer(**customer_data.dict())
        self.db.add(customer)
        await self.db.commit()
        await self.db.refresh(customer)
        return customer

    async def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        result = await self.db.execute(select(Customer).filter(Customer.id == customer_id))
        return result.scalars().first()

    async def list_customers(self) -> List[Customer]:
        result = await self.db.execute(select(Customer))
        return result.scalars().all()

    async def update_customer(self, db_customer: Customer, update_data: CustomerUpdate) -> Customer:
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(db_customer, field, value)
        await self.db.commit()
        await self.db.refresh(db_customer)
        return db_customer

    async def delete_customer(self, db_customer: Customer):
        await self.db.delete(db_customer)
        await self.db.commit()
