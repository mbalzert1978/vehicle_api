import datetime

from vehicle_api.utils import utils


def test_utc_now_when_called_should_return_utc_time_aware_datetime_object() -> None:
    """
    Given: None
    When: utc_now() is called
    Then: utc_now() should return a time aware datetime.datetime object
    """
    now = utils.utc_now()

    assert isinstance(now, datetime.datetime)
    assert now.tzinfo == datetime.timezone.utc
