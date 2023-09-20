"""Pydantic models."""
import json

from pydantic import BaseModel, validator


class VehicleBase(BaseModel):
    """Base vehicle model."""

    name: str
    year_of_manufacture: int
    ready_to_drive: bool = False


class VehicleCreate(VehicleBase):
    """Vehicle create model."""

    body: dict


class VehicleUpdate(BaseModel):
    """Vehicle update model."""

    name: str | None = None
    year_of_manufacture: int | None = None
    body: dict | None = None
    ready_to_drive: bool = False


class VehicleInDBBase(VehicleBase):
    """Vehicle in DB model."""

    id: int | None = None  # noqa: A003
    name: str
    year_of_manufacture: int
    body: dict
    ready_to_drive: bool = False

    class Config:
        """Pydantic config."""

        orm_mode = True

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


class Vehicle(VehicleInDBBase):
    """Vehicle model."""


class VehicleInDB(VehicleInDBBase):
    """Vehicle in DB model."""
