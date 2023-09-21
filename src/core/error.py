"""Custom exceptions."""


class HTTPError(Exception):

    """Base class for HTTP errors."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
