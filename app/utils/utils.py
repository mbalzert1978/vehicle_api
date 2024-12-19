import datetime

import uuid_utils as uuid


def utc_now() -> datetime.datetime:
    """Returns a utc timezone aware datetime object."""
    return datetime.datetime.now(tz=datetime.timezone.utc)


def is_valid_uuid7(value: str) -> bool:
    """
    Check whether a string is a valid v4 uuid.
    """
    try:
        return bool(uuid.UUID(value, version=7))
    except ValueError:
        return False
