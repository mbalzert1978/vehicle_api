import dataclasses
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclasses.dataclass
class ListResponse(Generic[T]):
    data: list[T]


@dataclasses.dataclass
class Response(Generic[T]):
    data: T
