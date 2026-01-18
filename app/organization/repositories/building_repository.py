from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.organization.repositories.base import BaseRepository
from app.organization.models.building import Building


class BuildingRepository(BaseRepository[Building]):
    """Репозиторий, инкапсулирующий логику взаимодействия с таблицей зданий."""

    def __init__(self, db: AsyncSession):
        super().__init__(Building, db)

    async def get_with_organizations(self, id: int) -> Building | None:
        """Метод для получения здания и организаций, расположенных в нем."""
        result = await self.db.execute(
            select(Building)
            .options(selectinload(Building.organizations))
            .where(Building.id == id)
        )
        return result.scalar_one_or_none()

    async def get_in_bounds(self, min_lat: float, max_lat: float, min_lon: float, max_lon: float) -> list[Building]:
        """Метод для получения зданий в определенной зоне по координатам."""
        result = await self.db.execute(
            select(Building).where(
                and_(
                    Building.latitude.between(min_lat, max_lat),
                    Building.longitude.between(min_lon, max_lon),
                )
            )
        )
        return list(result.scalars().all())
