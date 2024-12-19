import datetime


def utc_now() -> datetime.datetime:
    """Returns a utc timezone aware datetime object."""
    return datetime.datetime.now(tz=datetime.timezone.utc)
