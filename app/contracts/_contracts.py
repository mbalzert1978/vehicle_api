from collections.abc import Sized

from .exceptions import (
    ArgumentNull,
    ArgumentNullOrEmpty,
    ArgumentNullOrWhiteSpace,
    ArgumentTypeMismatch,
)

NULL_MSG = "Argument cannot be null."
NULL_OR_EMPTY_MSG = "Argument cannot be null or empty."
NULL_OR_WHITESPACE_MSG = "Argument cannot be null or whitespace."
INVALID_TYPE_MSG = "Expected argument of type {}, got {}."
EMPTY_LENGTH = 0


def requires_not_null[T](arg: T) -> None:
    """
    Ensures that the given argument is not null.

    This function checks if the provided argument is not None. If the argument
    is None, it raises an ArgumentNull exception.

    Args:
        arg (T): The argument to be checked.

    Raises:
        ArgumentNull: If the argument is None.
    """
    if arg is not None:
        return
    raise ArgumentNull(NULL_MSG)


def requires_not_null_not_empty[T](arg: T) -> None:
    """
    Ensures that the given argument is not null and not empty.

    This function checks if the provided argument is not None and not empty.
    If the argument is None or empty, it raises an ArgumentNullOrEmpty exception.

    Args:
        arg (T): The argument to be checked.

    Raises:
        ArgumentNullOrEmpty: If the argument is None or empty.
    """
    requires_not_null(arg)
    if isinstance(arg, str) and arg.isspace():
        raise ArgumentNullOrWhiteSpace(NULL_OR_WHITESPACE_MSG)
    if isinstance(arg, Sized) and len(arg) == EMPTY_LENGTH:
        raise ArgumentNullOrEmpty(NULL_OR_EMPTY_MSG)
    return


def requires_type[T](arg: T, valid: type) -> None:
    """
    Ensures that the given argument is of the specified type.

    This function checks if the provided argument is of the specified type.
    If the argument is not of the expected type, it raises an ArgumentTypeMismatch exception.

    Args:
        arg (T): The argument to be checked.
        valid (type): The expected type of the argument.
    Raises:
        ArgumentTypeMismatch: If the argument is not of the expected type.
    """
    if isinstance(arg, valid):
        return
    err_msg = INVALID_TYPE_MSG.format(valid.__name__, type(arg).__name__)
    raise ArgumentTypeMismatch(err_msg)
