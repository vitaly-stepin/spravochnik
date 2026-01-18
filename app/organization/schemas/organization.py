from datetime import datetime
from pydantic import BaseModel
from app.organization.schemas.building import BuildingSchema
from app.organization.schemas.activity import ActivitySchema
from app.organization.schemas.phone_number import PhoneNumberBase


class OrganizationBase(BaseModel):
    name: str
    building_id: int


class OrganizationSchema(OrganizationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrganizationDetail(OrganizationSchema):
    building: BuildingSchema
    phone_numbers: list[PhoneNumberBase] = []
    activities: list[ActivitySchema] = []
