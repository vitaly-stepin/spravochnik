from math import radians, cos, sin, asin, sqrt
from sqlalchemy.ext.asyncio import AsyncSession
from app.organization.repositories.organization_repository import OrganizationRepository
from app.organization.repositories.activity_repository import ActivityRepository
from app.organization.models.organization import Organization


class OrganizationService:
    def __init__(self, db: AsyncSession):
        self.org_repo = OrganizationRepository(db)
        self.activity_repo = ActivityRepository(db)

    async def get_by_id(self, org_id: int) -> Organization | None:
        return await self.org_repo.get_with_relations(org_id)

    async def get_by_name(self, name: str) -> Organization | None:
        return await self.org_repo.get_by_name(name)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Organization]:
        return await self.org_repo.get_all_with_relations(skip, limit)

    async def get_by_building(
        self, building_id: int, skip: int = 0, limit: int = 100
    ) -> list[Organization]:
        return await self.org_repo.get_by_building_id(building_id, skip, limit)

    async def get_by_activity(
        self, activity_id: int, skip: int = 0, limit: int = 100
    ) -> list[Organization]:
        """Get organizations by activity, including nested child activities."""
        activity_ids = await self.activity_repo.get_descendant_ids(activity_id)
        return await self.org_repo.get_by_activity_ids(activity_ids, skip, limit)

    async def get_in_radius(
        self, latitude: float, longitude: float, radius_km: float
    ) -> list[Organization]:
        """Get organizations within radius using bounding box pre-filter + Haversine."""
        lat_diff = radius_km / 111.0
        lon_diff = radius_km / (111.0 * cos(radians(latitude)))

        candidates = await self.org_repo.get_in_coordinate_bounds(
            latitude - lat_diff,
            latitude + lat_diff,
            longitude - lon_diff,
            longitude + lon_diff,
        )

        return [
            org
            for org in candidates
            if self._haversine(
                latitude, longitude, org.building.latitude, org.building.longitude
            )
            <= radius_km
        ]

    async def get_in_area(
        self, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ) -> list[Organization]:
        return await self.org_repo.get_in_coordinate_bounds(
            min_lat, max_lat, min_lon, max_lon
        )

    @staticmethod
    def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        return 6371.0 * 2 * asin(sqrt(a))
