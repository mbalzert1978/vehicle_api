from pydantic import BaseModel


class VehicleBase(BaseModel):
    name: str | None = None
    year_of_manufacture: int | None = None
    body: str | None = None
    ready_to_drive: bool = False


class VehicleCreate(VehicleBase):
    name: str
    year_of_manufacture: int
    body: str
    ready_to_drive: bool = False


class VehicleUpdate(VehicleBase):
    name: str | None = None
    year_of_manufacture: int | None = None
    body: str | None = None
    ready_to_drive: bool = False


class VehicleInDBBase(VehicleBase):
    id: int | None = None  # noqa: A003
    name: str | None = None
    year_of_manufacture: int | None = None
    body: str | None = None
    ready_to_drive: bool = False

    class Config:
        orm_mode = True


class Vehicle(VehicleInDBBase):
    pass


class VehicleInDB(VehicleInDBBase):
    pass
