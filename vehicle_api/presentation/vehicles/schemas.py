"""Pydantic models."""

import dataclasses
import datetime
import functools
import typing
import uuid

import uuid_utils
from pydantic import ConfigDict, Field, Json

from presentation.schemas import CustomModel
from presentation.utils.utils import utc_now

T = typing.TypeVar("T")


@dataclasses.dataclass
class DataMany(typing.Generic[T]):
    data: list[T]


@dataclasses.dataclass
class DataOne(typing.Generic[T]):
    data: T


DESCRIPTION_NAME = "The name of the vehicle."
DESCRIPTION_MY = "The manufacturing year of the vehicle."
DESCRIPTION_DRIVABLE = "Whether the vehicle is drivable."
DESCRIPTION_BODY = "Additional information about the vehicle in the form of a dictionary."

field_name = functools.partial(Field, description=DESCRIPTION_NAME, examples=["Audi"])
field_year = functools.partial(Field, description=DESCRIPTION_MY, le=utc_now().year, examples=[1999])
field_drivable = functools.partial(Field, description=DESCRIPTION_DRIVABLE)
field_body = functools.partial(Field, description=DESCRIPTION_BODY, examples=[dict(color="black")])


class FilterVehicle(CustomModel):
    """Vehicle filter model."""

    name: str | None = None
    manufacturing_year: int | None = None
    is_drivable: bool | None = None


class CreateVehicle(CustomModel):
    """Vehicle create model."""

    id: uuid.UUID = Field(default_factory=uuid_utils.uuid7)
    name: str = field_name()
    manufacturing_year: int = field_year(default=utc_now().year)
    is_drivable: bool = field_drivable(default=False)
    body: dict = field_body(default_factory=dict)


class UpdateVehicle(CustomModel):
    """Vehicle update model."""

    name: str | None = field_name(default=None)
    manufacturing_year: int | None = field_year(default=None)
    is_drivable: bool | None = field_drivable(default=None)
    body: dict | None = field_body(default=None)


class VehicleFromDatabase(CreateVehicle):
    """Vehicle in DB model."""

    model_config = ConfigDict(from_attributes=True, extra="allow")
    id: uuid.UUID
    body: Json | dict
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None
