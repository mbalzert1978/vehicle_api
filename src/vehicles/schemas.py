"""Pydantic models."""

import dataclasses
import datetime
import functools
import typing
import uuid

import uuid_utils
from pydantic import ConfigDict, Field, Json

from src.schemas import CustomModel
from src.utils.utils import utc_now

T = typing.TypeVar("T")


@dataclasses.dataclass
class DataMany(typing.Generic[T]):
    data: list[T]


@dataclasses.dataclass
class DataOne(typing.Generic[T]):
    data: T


DESCRIPTION_NAME = "The name of the vehicle."
DESCRIPTION_MY = "The manufacturing year of the vehicle."
DESCRIPTION_DRIVEABLE = "Whether the vehicle is driveable."
DESCRIPTION_BODY = "Additional information about the vehicle in the form of a dictionary."

field_name = functools.partial(Field, description=DESCRIPTION_NAME, examples=["Audi"])
field_year = functools.partial(Field, description=DESCRIPTION_MY, le=utc_now().year, examples=[1999])
field_driveable = functools.partial(Field, description=DESCRIPTION_DRIVEABLE)
field_body = functools.partial(Field, description=DESCRIPTION_BODY, examples=[dict(color="black")])


class FilterVehicle(CustomModel):
    """Vehicle filter model."""

    name: str | None = None
    manufacturing_year: int | None = None
    is_driveable: bool | None = None


class CreateVehicle(CustomModel):
    """Vehicle create model."""

    id: uuid.UUID = Field(default_factory=uuid_utils.uuid7)
    name: str = field_name()
    manufacturing_year: int = field_year(default=utc_now().year)
    is_driveable: bool = field_driveable(default=False)
    body: dict = field_body(default_factory=dict)


class UpdateVehicle(CustomModel):
    """Vehicle update model."""

    name: str | None = field_name(default=None)
    manufacturing_year: int | None = field_year(default=None)
    is_driveable: bool | None = field_driveable(default=None)
    body: dict | None = field_body(default=None)


class VehicleFromDatabase(CreateVehicle):
    """Vehicle in DB model."""

    model_config = ConfigDict(from_attributes=True, extra="allow")
    id: uuid.UUID
    body: Json | dict
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
