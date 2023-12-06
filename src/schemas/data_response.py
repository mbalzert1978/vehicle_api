import dataclasses


@dataclasses.dataclass
class DataResponse[T]:
    data: list[T]
