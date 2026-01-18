from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth.dependencies import get_api_key
from app.organization.services.building_service import BuildingService
from app.organization.schemas.building import BuildingSchema

router = APIRouter(
    prefix="/buildings",
    tags=["Buildings"],
    dependencies=[Depends(get_api_key)],
)


@router.get("/", response_model=list[BuildingSchema])
async def list_buildings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    service = BuildingService(db)
    return await service.get_all(skip, limit)


@router.get("/{building_id}", response_model=BuildingSchema)
async def get_building(
    building_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = BuildingService(db)
    building = await service.get_by_id(building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building
