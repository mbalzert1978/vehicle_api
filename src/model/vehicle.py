"""Model."""

import abc
import datetime


class Base(abc.ABC):

    """Base Model."""

    @abc.abstractmethod
    def dump(self) -> dict:
        """Dump Model."""

    @abc.abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError


def _get_current_year() -> int:
    return datetime.datetime.now(tz=datetime.timezone.utc).date().year


class Vehicle(Base):

    """Vehicle Model."""

    def __init__(self,
                 name: str = "default",
                 year_of_manufacture: int | None = None,
                 body: dict | None = None,
                 *,
                 ready_to_drive: bool = False) -> None:
        self.name = name
        self.year_of_manufacture = year_of_manufacture or _get_current_year()
        self.body = body or {}
        self.ready_to_drive = ready_to_drive

    def dump(self) -> dict:
        """Dump Vehicle Model."""
        return self.__dict__

    def __repr__(self) -> str:
        return (f"Vehicle(name={self.name}, "
                f"year_of_manufacture={self.year_of_manufacture}, "
                f"body={self.body}, "
                f"ready_to_drive={self.ready_to_drive})")
