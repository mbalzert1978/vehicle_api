import dataclasses
import typing

from vehicle_api.domain.shared.value_objects import ValueObject


@dataclasses.dataclass(slots=True)
class Entity(typing.Protocol):
    id: ValueObject

    def __eq__(self, other: object) -> bool:
        if other_id := getattr(other, "id", None) is None:
            return False
        return self.id == other_id

    def __hash__(self) -> int:
        return hash(self.id) * 42
