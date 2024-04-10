"""Pydantic models."""

import json

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from src.utils.utils import utc_now

DESCIPTION_NAME = "The name of the vehicle."
DESCRIPTION_YOM = "The year of manufacture for the vehicle."
DESCRIPTION_RTD = "Whether the vehicle is ready to drive."
DESCRIPTION_BODY = "Additional information about the vehicle in the form of a dictionary."
NOW_YEAR = utc_now().year


class VehicleBase(BaseModel):
    """Base vehicle model."""

    name: str = Field(description=DESCIPTION_NAME, examples=["Audi"])
    year_of_manufacture: int = Field(
        description=DESCRIPTION_YOM,
        ge=2000,
        le=NOW_YEAR,
        examples=[1999],
        default=NOW_YEAR,
    )
    ready_to_drive: bool = Field(description=DESCRIPTION_RTD, default=False)


class VehicleCreate(VehicleBase):
    """Vehicle create model."""

    body: dict = Field(description=DESCRIPTION_BODY, default_factory=dict, examples=[dict(color="black")])

    @field_validator("body", mode="before")
    @classmethod
    def parse_body(cls, v: str, _: ValidationInfo) -> dict:
        """
        Parse the body value as JSON.

        Args:
        ----
        v: The value of the 'body' field.

        Returns:
        -------
        The parsed JSON data if 'v' is a string, otherwise the original value.

        """
        return json.loads(v) if isinstance(v, str) else v


class VehicleUpdate(BaseModel):
    """Vehicle update model."""

    name: str | None = Field(description=DESCIPTION_NAME, examples=["Audi"], default=None)
    year_of_manufacture: int | None = Field(
        description=DESCRIPTION_YOM,
        ge=1980,
        le=NOW_YEAR,
        examples=[1999],
        default=None,
    )
    body: dict | None = Field(description=DESCRIPTION_BODY, default_factory=dict, examples=[dict(color="black")])
    ready_to_drive: bool = Field(description=DESCRIPTION_RTD, default=None)


class VehicleInDBBase(VehicleCreate):
    """Vehicle in DB model."""

    id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class Vehicle(VehicleInDBBase):
    """Vehicle model."""


class VehicleInDB(VehicleInDBBase):
    """Vehicle in DB model."""
