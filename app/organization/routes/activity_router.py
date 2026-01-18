from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth.dependencies import get_api_key
from app.organization.models.activity import Activity
from app.organization.services.activity_service import ActivityService
from app.organization.schemas.activity import ActivitySchema, ActivityTree, ActivityWithChildren

router = APIRouter(
    prefix="/activities",
    tags=["Activities"],
    dependencies=[Depends(get_api_key)],
)


@router.get("/", response_model=list[ActivitySchema])
async def list_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> list[Activity]:
    service = ActivityService(db)
    return await service.get_all(skip, limit)


@router.get("/tree", response_model=list[ActivityTree])
async def get_activity_tree(db: AsyncSession = Depends(get_db)) -> list[Activity]:
    service = ActivityService(db)
    return await service.get_tree()


@router.get("/{activity_id}", response_model=ActivityWithChildren)
async def get_activity(activity_id: int, db: AsyncSession = Depends(get_db)) -> Activity:
    service = ActivityService(db)
    activity = await service.get_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity
