from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth.dependencies import get_api_key
from app.organization.services.organization_service import OrganizationService
from app.organization.schemas.organization import OrganizationDetail

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
    dependencies=[Depends(get_api_key)],
)


@router.get("/", response_model=list[OrganizationDetail])
async def list_organizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    service = OrganizationService(db)
    return await service.get_all(skip, limit)


@router.get("/search/radius", response_model=list[OrganizationDetail])
async def search_in_radius(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(..., gt=0, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = OrganizationService(db)
    return await service.get_in_radius(latitude, longitude, radius_km)


@router.get("/search/area", response_model=list[OrganizationDetail])
async def search_in_area(
    min_lat: float = Query(..., ge=-90, le=90),
    max_lat: float = Query(..., ge=-90, le=90),
    min_lon: float = Query(..., ge=-180, le=180),
    max_lon: float = Query(..., ge=-180, le=180),
    db: AsyncSession = Depends(get_db),
):
    service = OrganizationService(db)
    return await service.get_in_area(min_lat, max_lat, min_lon, max_lon)


@router.get("/by-building/{building_id}", response_model=list[OrganizationDetail])
async def get_by_building(
    building_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    service = OrganizationService(db)
    return await service.get_by_building(building_id, skip, limit)


@router.get("/by-activity/{activity_id}", response_model=list[OrganizationDetail])
async def get_by_activity(
    activity_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    service = OrganizationService(db)
    return await service.get_by_activity(activity_id, skip, limit)


@router.get("/by-name/{name}", response_model=OrganizationDetail)
async def get_by_name(
    name: str,
    db: AsyncSession = Depends(get_db),
):
    service = OrganizationService(db)
    org = await service.get_by_name(name)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.get("/{organization_id}", response_model=OrganizationDetail)
async def get_organization(
    organization_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = OrganizationService(db)
    org = await service.get_by_id(organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org
