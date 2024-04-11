import dataclasses


@dataclasses.dataclass
class ListResponse[T]:
    data: list[T]


@dataclasses.dataclass
class Response[T]:
    data: T
