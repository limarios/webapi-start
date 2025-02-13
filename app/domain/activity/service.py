from typing import List, Optional
from app.domain.activity.repository import ActivityRepository
from app.domain.activity.schemas import ActivityCreate, ActivityRead, ActivityUpdate

class ActivityService:
    def __init__(self, repo: ActivityRepository):
        self.repo = repo

    async def create_activity(self, activity_data: ActivityCreate) -> ActivityRead:
        activity = await self.repo.create_activity(activity_data)
        return ActivityRead.from_orm(activity)

    async def get_activity(self, activity_id: int) -> Optional[ActivityRead]:
        activity = await self.repo.get_activity_by_id(activity_id)
        return ActivityRead.from_orm(activity) if activity else None

    async def list_activities(self) -> List[ActivityRead]:
        activities = await self.repo.list_activities()
        return [ActivityRead.from_orm(a) for a in activities]

    async def update_activity(self, activity_id: int, update_data: ActivityUpdate) -> Optional[ActivityRead]:
        activity = await self.repo.get_activity_by_id(activity_id)
        if not activity:
            return None
        updated_activity = await self.repo.update_activity(activity, update_data)
        return ActivityRead.from_orm(updated_activity)

    async def delete_activity(self, activity_id: int) -> bool:
        activity = await self.repo.get_activity_by_id(activity_id)
        if not activity:
            return False
        await self.repo.delete_activity(activity)
        return True
