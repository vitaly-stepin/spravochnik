from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.organization.repositories.base import BaseRepository
from app.organization.models.activity import Activity


class ActivityRepository(BaseRepository[Activity]):
    """Репозиторий, инкапсулирующий логику взаимодействия с таблицей видов деятельности."""

    def __init__(self, db: AsyncSession):
        super().__init__(Activity, db)

    async def get_with_children(self, id: int) -> Activity | None:
        """Метод для получения вида деятельности, включая его подвиды (до 3 уровней)."""
        result = await self.db.execute(
            select(Activity)
            .options(
                selectinload(Activity.children)
                .selectinload(Activity.children)
                .selectinload(Activity.children)
            )
            .where(Activity.id == id)
        )
        return result.scalar_one_or_none()

    async def get_root_activities(self) -> list[Activity]:
        """Метод для получения видов деятельности первого уровня (с подвидами до 3 уровней)."""
        result = await self.db.execute(
            select(Activity)
            .options(
                selectinload(Activity.children)
                .selectinload(Activity.children)
                .selectinload(Activity.children)
            )
            .where(Activity.parent_id.is_(None))
        )
        return list(result.scalars().all())

    async def get_descendant_ids(self, activity_id: int) -> list[int]:
        """Метод для получения id вида деятельности и его подвидов (максимально 3 уровня)."""
        ids = [activity_id]

        level2 = await self.db.execute(
            select(Activity.id).where(Activity.parent_id == activity_id)
        )
        level2_ids = [r[0] for r in level2.all()]
        ids.extend(level2_ids)

        if level2_ids:
            level3 = await self.db.execute(
                select(Activity.id).where(Activity.parent_id.in_(level2_ids))
            )
            ids.extend([r[0] for r in level3.all()])

        return ids
