import abc
import uuid
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ValueObject(abc.ABC, Generic[T]):

    @property
    @abc.abstractmethod
    def value(self) -> T:
        raise NotImplementedError


@dataclass(frozen=True)
class GUID(ValueObject):
    guid: uuid.UUID = field(default_factory=uuid.uuid4)

    @property
    def value(self) -> T:
        return self.guid

def main():
    g = GUID()
    print(g.value)


if __name__ == '__main__':
    main()
