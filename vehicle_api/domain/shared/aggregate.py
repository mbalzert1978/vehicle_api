import dataclasses

from .entities import Entity


@dataclasses.dataclass(eq=False, slots=True)
class AggregateRoot(Entity): ...
