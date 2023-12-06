import pytest

from src.core.error import HTTPError
from src.crud import AbstractRepository
from src.service import services
from tests.stubs import Stub


def test_service_create():
    repository = Stub(spec=AbstractRepository)
    services.create(repository, "to_create")

    expected = [(), { "to_create": "to_create"}]

    assert repository.attr_stub.commands == expected


def test_service_get_happy():
    repository = Stub(spec=AbstractRepository, return_value=1)
    services.get( repository, 1)

    expected = [(), { "id": 1, "default": None}]

    assert repository.attr_stub.commands == expected


def test_service_get_not_found():
    repository = Stub(spec=AbstractRepository)

    with pytest.raises(HTTPError):
        services.get( repository, 1)


def test_service_filter_name():
    repository = Stub(spec=AbstractRepository)
    services.list(
        repository=repository,
        filter_by={"name": "test"},
    )

    expected = [(), {"filter_by": {"name": "test"}}]

    assert repository.attr_stub.commands == expected


def test_service_filter_year():
    repository = Stub(spec=AbstractRepository)
    services.list(
        repository=repository,
        filter_by={"year_of_manufacture": 2023},
    )

    expected = [(), {"filter_by": {"year_of_manufacture": 2023}}]

    assert repository.attr_stub.commands == expected


def test_service_filter_ready():
    repository = Stub(spec=AbstractRepository)
    services.list(
        repository=repository,
        filter_by={"ready_to_drive": False},
    )

    expected = [(), {"filter_by": {"ready_to_drive": False}}]

    assert repository.attr_stub.commands == expected


def test_update_negative():
    repository = Stub(spec=AbstractRepository)

    with pytest.raises(HTTPError):
        services.update( repository, 1, "to_update")


def test_delete_negative():
    repository = Stub(spec=AbstractRepository)

    with pytest.raises(HTTPError):
        services.delete( repository, 1)
