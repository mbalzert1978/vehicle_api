import typing

from vehicle_api.domain.error import Error

T = typing.TypeVar("T")


class Result(typing.Generic[T]):
    def __init__(self, *, is_success: bool, value: typing.Optional[T] = None, error: Error) -> None:
        if is_success and error is not Error.none() or not is_success and error is Error.none():
            err = "Either success or failure must be specified."
            raise ValueError(err)
        self.is_success = is_success
        self.value = value
        self.error = error

    def __repr__(self) -> str:
        return f"Result(is_success={self.is_success}, value={self.value}, error={self.error})"

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def success(cls, value: T) -> typing.Self:
        return cls(is_success=True, value=value, error=Error.none())

    @classmethod
    def failure(cls, error: Error) -> typing.Self:
        return cls(is_success=False, error=error)

    @property
    def is_failure(self) -> bool:
        return not self.is_success

    def unwrap(self) -> T:
        if self.value is None:
            err = "Result does not contain a value."
            raise ValueError(err)
        if self.is_failure:
            err = "Result is a failure."
            raise ValueError(err)
        return self.value
