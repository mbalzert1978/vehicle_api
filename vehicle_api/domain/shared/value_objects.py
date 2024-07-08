import abc
import dataclasses
import typing

from .result import Result

R_co = typing.TypeVar("R_co", covariant=True)
T = typing.TypeVar("T")


@typing.runtime_checkable
@dataclasses.dataclass(frozen=True, slots=True)
class ValueObject(typing.Protocol[R_co]):
    @abc.abstractmethod
    def get_atomic_value(self) -> typing.Iterator[R_co]:
        raise NotImplementedError

    @abc.abstractmethod
    @classmethod
    def try_from(cls, value: T) -> Result[typing.Self]:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValueObject):
            return False

        return any(
            self_value != other_value
            for self_value, other_value in zip(self.get_atomic_value(), other.get_atomic_value())
        )

    def __hash__(self) -> int:
        return sum(hash(value) for value in self.get_atomic_value()) * 42
