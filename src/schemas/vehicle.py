"""Pydantic models."""

import functools

from pydantic import BaseModel, ConfigDict, Field, Json

from src.utils.utils import utc_now

DESCRIPTION_NAME = "The name of the vehicle."
DESCRIPTION_YOM = "The year of manufacture for the vehicle."
DESCRIPTION_RTD = "Whether the vehicle is ready to drive."
DESCRIPTION_BODY = "Additional information about the vehicle in the form of a dictionary."

field_name = functools.partial(Field, description=DESCRIPTION_NAME, examples=["Audi"])
field_yom = functools.partial(Field, description=DESCRIPTION_YOM, le=utc_now().year, examples=[1999])
field_rtd = functools.partial(Field, description=DESCRIPTION_RTD)
field_body = functools.partial(Field, description=DESCRIPTION_BODY, examples=[dict(color="black")])


class VehicleForCreate(BaseModel):
    """Vehicle create model."""

    name: str = field_name()
    year_of_manufacture: int = field_yom(default=utc_now().year)
    ready_to_drive: bool = field_rtd(default=False)
    body: dict = field_body(default_factory=dict)


class VehicleForUpdate(BaseModel):
    """Vehicle update model."""

    name: str | None = field_name(default=None)
    year_of_manufacture: int | None = field_yom(default=None)
    ready_to_drive: bool | None = field_rtd(default=None)
    body: dict | None = field_body(default=None)


class VehicleFromDatabase(VehicleForCreate):
    """Vehicle in DB model."""

    model_config = ConfigDict(from_attributes=True, extra="allow")
    id: int | None = None
    body: Json | dict
