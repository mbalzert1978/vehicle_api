import json

from pydantic import BaseModel, validator


class VehicleBase(BaseModel):
    name: str | None = None
    year_of_manufacture: int | None = None
    body: dict | None = None
    ready_to_drive: bool = False


class VehicleCreate(VehicleBase):
    name: str
    year_of_manufacture: int
    body: dict
    ready_to_drive: bool = False


class VehicleUpdate(VehicleBase):
    name: str | None = None
    year_of_manufacture: int | None = None
    body: dict | None = None
    ready_to_drive: bool = False


class VehicleInDBBase(VehicleBase):
    id: int | None = None  # noqa: A003
    name: str | None = None
    year_of_manufacture: int | None = None
    body: dict | None = None
    ready_to_drive: bool = False

    class Config:
        orm_mode = True

    @validator("body", pre=True)
    @classmethod
    def parse_body(
        cls,
        v: str | dict | None,
    ) -> dict | None:
        return json.loads(v) if isinstance(v, str) else v


class Vehicle(VehicleInDBBase):
    pass


class VehicleInDB(VehicleInDBBase):
    pass
