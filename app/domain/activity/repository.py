from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.domain.activity.models import Activity
from app.domain.activity.schemas import ActivityCreate, ActivityUpdate

class ActivityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_activity(self, activity_data: ActivityCreate) -> Activity:
        activity = Activity(**activity_data.dict())
        self.db.add(activity)
        await self.db.commit()
        await self.db.refresh(activity)
        return activity

    async def get_activity_by_id(self, activity_id: int) -> Optional[Activity]:
        result = await self.db.execute(select(Activity).filter(Activity.id == activity_id))
        return result.scalars().first()

    async def list_activities(self) -> List[Activity]:
        result = await self.db.execute(select(Activity))
        return result.scalars().all()

    async def update_activity(self, db_activity: Activity, update_data: ActivityUpdate) -> Activity:
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(db_activity, field, value)
        await self.db.commit()
        await self.db.refresh(db_activity)
        return db_activity

    async def delete_activity(self, db_activity: Activity):
        await self.db.delete(db_activity)
        await self.db.commit()
