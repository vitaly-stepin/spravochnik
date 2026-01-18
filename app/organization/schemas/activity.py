from pydantic import BaseModel


class ActivityBase(BaseModel):
    name: str
    level: int
    parent_id: int | None = None


class ActivitySchema(ActivityBase):
    id: int

    model_config = {"from_attributes": True}


class ActivityWithChildren(ActivitySchema):
    children: list["ActivityWithChildren"] = []


class ActivityTree(ActivitySchema):
    children: list["ActivityTree"] = []
