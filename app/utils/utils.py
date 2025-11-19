import datetime
from typing import Final

import uuid_utils as uuid

UUID_VERSION_7: Final[int] = 7


def utc_now() -> datetime.datetime:
    """Return a UTC timezone-aware datetime object.

    Returns:
        A datetime object representing the current time in UTC timezone.
    """
    result = datetime.datetime.now(tz=datetime.timezone.utc)

    assert isinstance(result, datetime.datetime), "Result must be a datetime instance"
    assert result.tzinfo is not None, "Result must be timezone-aware"
    assert result.tzinfo == datetime.timezone.utc, "Result must be in UTC timezone"

    return result


def is_valid_uuid7(value: str) -> bool:
    """Check whether a string is a valid UUID version 7.

    Args:
        value: The string to validate as a UUID7.

    Returns:
        True if the string is a valid UUID7, False otherwise.
    """
    assert isinstance(value, str), "Value must be a string"
    assert value.strip(), "Value must not be empty"

    try:
        uuid_obj = uuid.UUID(value, version=UUID_VERSION_7)
        assert isinstance(uuid_obj, uuid.UUID), (
            "UUID object must be an instance of UUID"
        )
    except ValueError:
        return False

    result = bool(uuid_obj)
    assert isinstance(result, bool), "Result must be a boolean"

    return result
