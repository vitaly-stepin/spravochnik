from sqlalchemy.ext.asyncio import AsyncSession
from app.organization.repositories.building_repository import BuildingRepository
from app.organization.models.building import Building


class BuildingService:
    def __init__(self, db: AsyncSession):
        self.repo = BuildingRepository(db)

    async def get_by_id(self, building_id: int) -> Building | None:
        return await self.repo.get_with_organizations(building_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Building]:
        return await self.repo.get_all(skip, limit)
