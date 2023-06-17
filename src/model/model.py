from datetime import datetime

from pydantic import BaseModel, Field

from src.model.orm import TransportMode


class Base(BaseModel):
    class Config:
        orm_mode = True


class Brand(Base):
    brand_id: int | None = None
    name: str


class Color(Base):
    color_id: int | None = None
    name: str


class TransportationMode(Base):
    transportation_mode_id: int | None = None
    name: TransportMode


class Address(Base):
    address_id: int | None = None
    street: str
    city: str
    state: str
    zip_code: str


class Owner(Base):
    owner_id: int | None = None
    name: str
    phone: str
    address: Address


class VehicleBase(Base):
    model: str
    year: datetime
    transportation_modes: list[TransportationMode] = Field(
        default=[TransportMode.LAND],
    )


class Vehicle(VehicleBase):
    vehicle_id: int | None = None
    brand: Brand
    color: Color
    owner: Owner | None = None


class VehicleCreate(VehicleBase):
    brand_id: int | None = None
    color_id: int | None = None
    owner_id: int | None = None


class VehicleUpdate(VehicleBase):
    brand_id: int | None = None
    color_id: int | None = None
    owner_id: int | None = None
