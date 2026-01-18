from sqlalchemy.ext.asyncio import AsyncSession
from app.organization.repositories.activity_repository import ActivityRepository
from app.organization.models.activity import Activity


class ActivityService:
    def __init__(self, db: AsyncSession):
        self.repo = ActivityRepository(db)

    async def get_by_id(self, activity_id: int) -> Activity | None:
        return await self.repo.get_with_children(activity_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Activity]:
        return await self.repo.get_all(skip, limit)

    async def get_tree(self) -> list[Activity]:
        return await self.repo.get_root_activities()
