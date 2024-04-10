import abc


class Base(abc.ABC):
    """Base Model."""

    @abc.abstractmethod
    def model_dump(self) -> dict:
        """Dump Model."""

    @abc.abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError
