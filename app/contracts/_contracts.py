from typing import NoReturn

from .exceptions import (
    ArgumentNull,
    ArgumentNullOrEmpty,
    ArgumentNullOrWhiteSpace,
    ArgumentTypeMismatch,
)


def requires_not_null[T](arg: T) -> NoReturn:
    """Checks if the argument is None and raises a ArgumentException if it is."""
    if arg is not None:
        return
    raise ArgumentNull("Argument cannot be None.")


def requires_not_null_not_empty[T](arg: T) -> NoReturn:
    """Checks if the argument is None or an empty sequence and raises a ArgumentException if it is."""
    match arg:
        case None:
            raise ArgumentNull("Argument cannot be None.")
        case str() as s if s.isspace():
            raise ArgumentNullOrWhiteSpace("Argument cannot be null or whitespace.")
        case _ as t if not t:
            raise ArgumentNullOrEmpty("Argument cannot be empty.")
        case _:
            return


def requires_type[T](arg: T, expected_type: type) -> NoReturn:
    """Checks if the argument is of the expected type and raises a ArgumentException if it is not."""
    if isinstance(arg, expected_type):
        return
    raise ArgumentTypeMismatch(
        f"Expected argument of type {expected_type.__name__}, got {type(arg).__name__}."
    )
