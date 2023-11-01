import pytest
from fastapi import HTTPException
from sqlalchemy.exc import OperationalError

from src.api.v1.endpoints.vehicle import list_vehicle
from src.crud.crud import AbstractRepository
from src.monads.result import Err
from tests.stubs import Stub


def test_list_vehicles_negative_uncaught():
    sess = Stub()
    repo = Stub(spec=AbstractRepository, return_value=Err(OperationalError("test", params=None, orig=Exception)))

    with pytest.raises(HTTPException):
        list_vehicle(session=sess, repository=repo)
