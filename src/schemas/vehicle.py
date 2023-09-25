"""Pydantic models."""
import datetime
import json

from pydantic import BaseModel, Field, validator


def _get_now_year() -> int:
    return datetime.datetime.now(tz=datetime.UTC).year


class VehicleBase(BaseModel):

    """Base vehicle model."""

    name: str = Field(description="The name of the vehicle.", example="Audi")
    year_of_manufacture: int = Field(
        description="The year of manufacture for the vehicle.",
        ge=2000,
        le=_get_now_year(),
        default=_get_now_year(),
    )
    ready_to_drive: bool = Field(description="Whether the vehicle is ready to drive.", default=False)


class VehicleCreate(VehicleBase):

    """Vehicle create model."""

    body: dict = Field(
        description="Additional information about the vehicle in the form of a dictionary.",
        default_factory=dict,
        example=dict(color="black"),
    )

    @validator("body", pre=True)
    @classmethod
    def parse_body(cls, v: str | dict) -> dict | None:
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

    name: str | None = Field(description="The name of the vehicle.", example="Audi", default=None)
    year_of_manufacture: int | None = Field(
        description="The year of manufacture for the vehicle.",
        ge=2000,
        le=_get_now_year(),
        default=None,
    )
    body: dict | None = Field(
        description="Additional information about the vehicle in the form of a dictionary.",
        default_factory=dict,
        example=None,
    )
    ready_to_drive: bool = Field(description="Whether the vehicle is ready to drive.", default=None)


class VehicleInDBBase(VehicleCreate):

    """Vehicle in DB model."""

    id: int | None = None  # noqa: A003

    class Config:

        """Pydantic config."""

        orm_mode = True


class Vehicle(VehicleInDBBase):

    """Vehicle model."""


class VehicleInDB(VehicleInDBBase):

    """Vehicle in DB model."""
