"""Model."""

import abc


class Base(abc.ABC):
    """Base Model."""

    @abc.abstractmethod
    def dump(self) -> dict:
        """Dump Model."""

    @abc.abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError


class Vehicle(Base):
    """Vehicle Model."""

    def __init__(self, name: str, year_of_manufacture: int, body: dict, *,
                 ready_to_drive: bool) -> None:
        self.name = name
        self.year_of_manufacture = year_of_manufacture
        self.body = body
        self.ready_to_drive = ready_to_drive

    def dump(self) -> dict:
        """Dump Vehicle Model."""
        return self.__dict__

    def __repr__(self) -> str:
        return (f"Vehicle(name={self.name}, "
                f"year_of_manufacture={self.year_of_manufacture}, "
                f"body={self.body}, "
                f"ready_to_drive={self.ready_to_drive})")
