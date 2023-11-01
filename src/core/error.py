"""Custom exceptions."""


class HTTPError(Exception):

    """Base class for HTTP errors."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail


class CreateError(Exception):
    """Error raised when trying to create a new object."""


class UnwrapError(Exception):
    def __init__(self, from_: BaseException) -> None:
        self.from_ = from_


class ReadOnlyError(Exception):
    """Error raised when trying to modify a read-only object."""


class NotFoundError(Exception):
    def init(self, id: int) -> None:
        self.id = id
