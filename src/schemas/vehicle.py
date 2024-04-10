"""Pydantic models."""

import functools

from pydantic import BaseModel, ConfigDict, Field, Json

from src.utils.utils import utc_now

DESCRIPTION_NAME = "The name of the vehicle."
DESCRIPTION_YOM = "The year of manufacture for the vehicle."
DESCRIPTION_RTD = "Whether the vehicle is ready to drive."
DESCRIPTION_BODY = "Additional information about the vehicle in the form of a dictionary."
NOW_YEAR = utc_now().year

FIELD_NAME = functools.partial(Field, description=DESCRIPTION_NAME, examples=["Audi"])
FIELD_YOM = functools.partial(Field, description=DESCRIPTION_YOM, le=NOW_YEAR, examples=[1999])
FIELD_RTD = functools.partial(Field, description=DESCRIPTION_RTD)
FIELD_BODY = functools.partial(Field, description=DESCRIPTION_BODY, examples=[dict(color="black")])


class VehicleForCreate(BaseModel):
    """Vehicle create model."""

    name: str = FIELD_NAME()
    year_of_manufacture: int = FIELD_YOM(default=NOW_YEAR)
    ready_to_drive: bool = FIELD_RTD(default=False)
    body: dict = FIELD_BODY(default_factory=dict)


class VehicleForUpdate(BaseModel):
    """Vehicle update model."""

    name: str | None = FIELD_NAME(default=None)
    year_of_manufacture: int | None = FIELD_YOM(default=None)
    ready_to_drive: bool | None = FIELD_RTD(default=None)
    body: dict | None = FIELD_BODY(default=None)


class VehicleFromDatabase(VehicleForCreate):
    """Vehicle in DB model."""

    model_config = ConfigDict(from_attributes=True, extra="allow")
    id: int | None = None
    body: Json | dict
