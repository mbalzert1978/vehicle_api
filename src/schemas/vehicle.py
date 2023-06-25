import json
from typing import NotRequired, TypedDict

from pydantic import BaseModel, validator


class VehicleData(TypedDict):
    color: NotRequired[str]
    kilometer: NotRequired[int]
    price: NotRequired[int]
    vehicle_type: NotRequired[str]


class VehicleBase(BaseModel):
    name: str | None = None
    year_of_manufacture: int | None = None
    body: VehicleData | None = None
    ready_to_drive: bool = False


class VehicleCreate(VehicleBase):
    name: str
    year_of_manufacture: int
    body: VehicleData
    ready_to_drive: bool = False


class VehicleUpdate(VehicleBase):
    name: str | None = None
    year_of_manufacture: int | None = None
    body: VehicleData | None = None
    ready_to_drive: bool = False


class VehicleInDBBase(VehicleBase):
    id: int | None = None  # noqa: A003
    name: str | None = None
    year_of_manufacture: int | None = None
    body: VehicleData | None = None
    ready_to_drive: bool = False

    class Config:
        orm_mode = True

    @validator("body", pre=True)
    @classmethod
    def parse_body(cls, v: str | dict | None) -> VehicleData | None:
        match v:
            case None:
                return None
            case str():
                return VehicleData(**json.loads(v))  # type:ignore[misc]
            case dict():
                return VehicleData(**v)  # type:ignore[misc]
            case _:
                err = f"Invalid body type: {v}"
                raise ValueError(err)


class Vehicle(VehicleInDBBase):
    pass


class VehicleInDB(VehicleInDBBase):
    pass
