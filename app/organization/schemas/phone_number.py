from pydantic import BaseModel


class PhoneNumberBase(BaseModel):
    number: str


class PhoneNumberSchema(PhoneNumberBase):
    id: int
    organization_id: int

    model_config = {"from_attributes": True}
