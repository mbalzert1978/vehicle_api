import dataclasses
import typing

from vehicle_api.domain.error import Error
from vehicle_api.domain.shared.result import Result
from vehicle_api.domain.shared.value_objects import ValueObject

T = typing.TypeVar("T")

MIN_YEAR = 1900
MAX_YEAR = 2100


@dataclasses.dataclass(frozen=True, slots=True)
class Year(ValueObject[int]):
    value: int

    def get_atomic_value(self) -> typing.Iterator[int]:
        yield self.value

    @classmethod
    def try_from(cls, value: T) -> Result[typing.Self]:
        if not isinstance(value, int):
            err = f"Invalid input type. Expected int, got {type(value).__name__}."
            return Result.failure(Error.bad_request(description=err))
        if value < MIN_YEAR or value > MAX_YEAR:
            err = f"Year must be between {MIN_YEAR} and {MAX_YEAR}, got {value}."
            return Result.failure(Error.bad_request(description=err))
        try:
            return Result.success(cls(value=value))
        except (ValueError, TypeError):
            err = "Failed to create Year object."
            return Result.failure(Error.internal_server_error(err))
