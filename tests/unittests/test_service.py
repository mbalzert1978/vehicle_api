import pytest

from src.core.error import HTTPError
from src.crud import AbstractRepository
from src.monads.option import Null
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

    expected = [(), {"session": "TestSession", "id": 1}]

    assert repository.attr_stub.commands == expected


def test_service_get_not_found():
    repository = Stub(spec=AbstractRepository, return_value=Null())

    with pytest.raises(HTTPError):
        services.get("TestSession", repository, 1)


def test_service_filter_name():
    repository = Stub(spec=AbstractRepository)
    services.list(
        session="TestSession",
        repository=repository,
        filter_by={"name": "test"},
    )

    expected = [("TestSession",), {"filter_by": {"name": "test"}}]

    assert repository.attr_stub.commands == expected


def test_service_filter_year():
    repository = Stub(spec=AbstractRepository)
    services.list(
        session="TestSession",
        repository=repository,
        filter_by={"year_of_manufacture": 2023},
    )

    expected = [("TestSession",), {"filter_by": {"year_of_manufacture": 2023}}]

    assert repository.attr_stub.commands == expected


def test_service_filter_ready():
    repository = Stub(spec=AbstractRepository)
    services.list(
        session="TestSession",
        repository=repository,
        filter_by={"ready_to_drive": False},
    )

    expected = [("TestSession",), {"filter_by": {"ready_to_drive": False}}]

    assert repository.attr_stub.commands == expected


def test_update_negative():
    repository = Stub(spec=AbstractRepository, return_value=Null())

    with pytest.raises(HTTPError):
        services.update("TestSession", repository, 1, "to_update")


def test_delete_negative():
    repository = Stub(spec=AbstractRepository, return_value=Null())

    with pytest.raises(HTTPError):
        services.delete("TestSession", repository, 1)
