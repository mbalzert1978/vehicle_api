"""Custom exceptions."""


class HTTPError(Exception):
    """Base class for HTTP errors."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail


class VehicleError(Exception):
    """Base class for vehicle errors."""


class GenericError(VehicleError):
    """Base class for generic errors."""
