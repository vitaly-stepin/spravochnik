from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.organization.repositories.base import BaseRepository
from app.organization.models.organization import Organization
from app.organization.models.building import Building
from app.organization.models.activity import Activity


class OrganizationRepository(BaseRepository[Organization]):
    """Репозиторий, инкапсулирующий логику взаимодействия с таблицей организаций."""

    def __init__(self, db: AsyncSession):
        super().__init__(Organization, db)

    async def get_with_relations(self, id: int) -> Organization | None:
        result = await self.db.execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
                selectinload(Organization.building),
            )
            .where(Organization.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Organization | None:
        result = await self.db.execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
                selectinload(Organization.building),
            )
            .where(Organization.name == name)
        )
        return result.scalar_one_or_none()

    async def get_all_with_relations(self, skip: int = 0, limit: int = 100) -> list[Organization]:
        """
        Метод для получения всех организаций. 
        Batchsize по дефолту 100. Обычно это настраивается через конфиг, но для экономии времени сделал простой вариант.
        """
        result = await self.db.execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
                selectinload(Organization.building),
            )
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_building_id(self, building_id: int, skip: int = 0, limit: int = 100) -> list[Organization]:
        result = await self.db.execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
                selectinload(Organization.building),
            )
            .where(Organization.building_id == building_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_activity_ids(self, activity_ids: list[int], skip: int = 0, limit: int = 100) -> list[Organization]:
        result = await self.db.execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
                selectinload(Organization.building),
            )
            .where(Organization.activities.any(Activity.id.in_(activity_ids)))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_in_coordinate_bounds(self, min_lat: float, max_lat: float, min_lon: float, max_lon: float) -> list[Organization]:
        result = await self.db.execute(
            select(Organization)
            .options(
                selectinload(Organization.phone_numbers),
                selectinload(Organization.activities),
                selectinload(Organization.building),
            )
            .join(Building)
            .where(
                and_(
                    Building.latitude.between(min_lat, max_lat),
                    Building.longitude.between(min_lon, max_lon),
                )
            )
        )
        return list(result.scalars().all())
