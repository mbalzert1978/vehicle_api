from __future__ import annotations

import dataclasses
import typing

from src.core.error import UnwrapError

T = typing.TypeVar("T", covariant=True)
E = typing.TypeVar("E", covariant=True)


@dataclasses.dataclass(frozen=True, slots=True)
class Ok[T]:
    __match_args__ = ("value",)

    value: T

    def __repr__(self) -> str:
        return f"Ok({repr(self.value)})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ok) and self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((True, self.value))

    def is_ok(self) -> typing.Literal[True]:
        return True

    def unwrap(self) -> T:
        return self.value

    def unwrap_or[U](self, _: U) -> T:
        return self.value

    def unwrap_or_raise(self, _: BaseException) -> T:
        return self.value

    def map[U](self, fn: typing.Callable[[T], U]) -> Result[U, E]:
        try:
            return Ok(fn(self.value))
        except Exception as exc:
            return Err(exc)


@dataclasses.dataclass(frozen=True, slots=True)
class Err[E]:
    __match_args__ = ("value",)

    value: E

    def __repr__(self) -> str:
        return f"Err({repr(self.value)})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Err) and self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((False, self.value))

    def is_ok(self) -> typing.Literal[False]:
        return False

    def unwrap(self) -> typing.NoReturn:
        raise UnwrapError(self.value)

    def unwrap_or[U](self, default: U) -> U:
        return default

    def unwrap_or_raise(self, exception: BaseException) -> typing.NoReturn:
        exc = UnwrapError(self.value)
        if not isinstance(exception, BaseException):
            raise exc
        raise exception

    def map[U](self, fn: typing.Callable[[E], U]) -> Result[U, E]:
        return self


Result: typing.TypeAlias = Ok[T] | Err[E]
