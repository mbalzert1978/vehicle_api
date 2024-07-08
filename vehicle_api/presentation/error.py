import dataclasses
from enum import StrEnum


class Error(StrEnum):
    """Errors."""

    GENERIC = "generic error."


class VehicleError(Exception):
    """Base class for all vehicle api related errors."""


@dataclasses.dataclass(frozen=True)
class InternalError(VehicleError):
    """Internal server error."""

    error: Error
