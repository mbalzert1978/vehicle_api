import pytest

from src.core.error import HTTPError
from src.crud import AbstractRepository
from src.service import services
from tests.stubs import Stub


def test_service_create():
    repository = Stub(spec=AbstractRepository)
    services.create("TestSession", repository, "to_create")

    expected = [(), {"session": "TestSession", "to_create": "to_create"}]

    assert repository.attr_stub.commands == expected


def test_service_get_happy():
    repository = Stub(spec=AbstractRepository, return_value=1)
    services.get("TestSession", repository, 1)

    expected = [(), {"session": "TestSession", "id": 1, "default": None}]

    assert repository.attr_stub.commands == expected

def test_service_get_not_found():
    repository = Stub(spec=AbstractRepository)

    with pytest.raises(HTTPError):
        services.get("TestSession", repository, 1)

def test_service_filter_name():
    repository = Stub(spec=AbstractRepository)
    services.filter_by("TestSession", repository, services.FilterBy.NAME, "test")

    expected = [(), {"session": "TestSession", "filter_by": {services.FilterBy.NAME: "test"}}]

    assert repository.attr_stub.commands == expected

def test_service_filter_year():
    repository = Stub(spec=AbstractRepository)
    services.filter_by("TestSession", repository, services.FilterBy.YEAR_OF_MANUFACTURE, "2020")

    expected = [(), {"session": "TestSession", "filter_by": {services.FilterBy.YEAR_OF_MANUFACTURE: 2020}}]

    assert repository.attr_stub.commands == expected

def test_parse_int():
    assert services._parse_int("123") == 123

def test_parse_int_negative():
    with pytest.raises(HTTPError):
        services._parse_int("-abc")

def test_parse_bool():
    assert services._parse_bool("True")
    assert services._parse_bool("1")
    assert services._parse_bool("t")
    assert services._parse_bool("yes")

def test_parse_bool_negative():
    assert not services._parse_bool("lksdjf+lkjasd")
    assert not services._parse_bool("0")

def test_service_filter_ready():
    repository = Stub(spec=AbstractRepository)
    services.filter_by("TestSession", repository, services.FilterBy.READY_TO_DRIVE, "True")

    expected = [(), {"session": "TestSession", "filter_by": {services.FilterBy.READY_TO_DRIVE: True}}]

    assert repository.attr_stub.commands == expected

def test_update_negative():
    repository = Stub(spec=AbstractRepository)

    with pytest.raises(HTTPError):
        services.update("TestSession", repository, 1, "to_update")

def test_delete_negative():
    repository = Stub(spec=AbstractRepository)

    with pytest.raises(HTTPError):
        services.delete("TestSession", repository, 1)
