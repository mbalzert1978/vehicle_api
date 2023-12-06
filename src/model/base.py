
import abc
import json


class Base(abc.ABC):

    """Base Model."""

    @abc.abstractmethod
    def dump(self) -> dict:
        """Dump Model."""

    @abc.abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    def to_json(self) -> str:
        return json.dumps(self.dump(), indent=4)
