import datetime


def utc_now() -> datetime.datetime:
    """Returns the UTC now datetime object."""
    return datetime.datetime.now(tz=datetime.timezone.utc)
