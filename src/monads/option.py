from __future__ import annotations

import dataclasses
import typing
from typing import Any

from src.core.error import UnwrapError, ReadOnlyError

T = typing.TypeVar("T", covariant=True)
N = typing.TypeVar("N", covariant=True)


@dataclasses.dataclass(frozen=True, slots=True)
class Some[T]:
    __match_args__ = ("value",)

    value: T

    def __repr__(self) -> str:
        return f"Some({repr(self.value)})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Some) and self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((True, self.value))

    def is_some(self) -> typing.Literal[True]:
        return True

    def unwrap(self) -> T:
        return self.value

    def unwrap_or[U](self, _: U) -> T:
        return self.value

    def unwrap_or_raise(self, _: BaseException) -> T:
        return self.value

    def map[U](self, fn: typing.Callable[[T], U]) -> Option[U]:
        match fn(self.value):
            case None:
                return Null()
            case _ as value:
                return Some(value)


@dataclasses.dataclass(slots=True)
class Null[N]:
    __match_args__ = ("value",)

    value: N = None

    def __setattr__(self, *_) -> None:
        if hasattr(self, "value"):
            raise ReadOnlyError(f"type({self.__class__.__name__}) is read-only")
        object.__setattr__(self, "value", None)

    def __repr__(self) -> str:
        return f"Null({repr(self.value)})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Null) and self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((False, 982006445019657274590041599673))

    def is_some(self) -> typing.Literal[False]:
        return False

    def unwrap(self) -> None:
        return self.value

    def unwrap_or[U](self, default: U) -> U:
        return default

    def unwrap_or_raise(self, exception: BaseException) -> typing.NoReturn:
        exc = UnwrapError(ValueError(self.value))
        if not isinstance(exception, BaseException):
            raise exc
        raise exception

    def map[U](self, _: typing.Callable[[N], U]) -> Option[U]:
        return self


Option: typing.TypeAlias = Some[T] | Null
