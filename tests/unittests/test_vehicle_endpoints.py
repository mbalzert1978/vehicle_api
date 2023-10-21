import pytest
from fastapi import HTTPException

from src.api.v1.endpoints.vehicle import list_vehicle
from src.core.error import HTTPError
from tests.stubs import Stub


def test_list_vehicles_negative():
    sess = Stub()
    repo = Stub(raise_on='list', raises=HTTPError(404, 'TestRaise'))

    with pytest.raises(HTTPException):
        list_vehicle(session=sess, repository=repo)


def test_list_vehicles_negative_uncaught():
    sess = Stub()
    repo = Stub(raise_on='list', raises=Exception)

    with pytest.raises(HTTPException):
        list_vehicle(session=sess, repository=repo)


def test_filter_vehicles_negative():
    sess = Stub()
    repo = Stub(raise_on='list', raises=HTTPError(404, 'TestRaise'))

    with pytest.raises(HTTPException):
        list_vehicle(session=sess, repository=repo, name='test')


def test_filter_vehicles_negative_uncaught():
    sess = Stub()
    repo = Stub(raise_on='list', raises=Exception)

    with pytest.raises(HTTPException):
        list_vehicle(session=sess, repository=repo, name='test')
