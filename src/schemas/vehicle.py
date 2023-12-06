"""Pydantic models."""
import datetime
import json

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

DESCIPTION_NAME = "The name of the vehicle."
DESCRIPTION_YOM = "The year of manufacture for the vehicle."
DESCRIPTION_RTD = "Whether the vehicle is ready to drive."
DESCRIPTION_BODY = "Additional information about the vehicle in the form of a dictionary."


def _get_year_now() -> int:
    return datetime.datetime.now(tz=datetime.UTC).year


class VehicleBase(BaseModel):

    """Base vehicle model."""

    name: str = Field(description=DESCIPTION_NAME, examples=["Audi"])
    year_of_manufacture: int = Field(
        description=DESCRIPTION_YOM,
        ge=2000,
        le=_get_year_now(),
        examples=[1999],
        default=_get_year_now(),
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
        le=_get_year_now(),
        examples=[1999],
        default=None,
    )
    body: dict | None = Field(description=DESCRIPTION_BODY, default_factory=dict, examples=[dict(color="black")])
    ready_to_drive: bool = Field(description=DESCRIPTION_RTD, default=None)


class VehicleInDBBase(VehicleCreate):

    """Vehicle in DB model."""

    id: int | None = None  # noqa: A003
    model_config = ConfigDict(from_attributes=True)


class Vehicle(VehicleInDBBase):

    """Vehicle model."""


class VehicleInDB(VehicleInDBBase):

    """Vehicle in DB model."""
