# type: ignore  # noqa: PGH003

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.crud.repository import CRUDRepository
from src.domain import models, schemas
from tests.data import I30, TEST_VEHICLE


def test_create(session: Session):
    """
    Given: A empty database session
    When: Creating a new vehicle using the Repository
    Then: The vehicle should be added to the database and the
        vehicle should be returned with a valid id
    """
    result = CRUDRepository(models.Vehicle).create(
        session,
        to_create=TEST_VEHICLE,
    )

    sql = text("SELECT * FROM vehicle WHERE id=:id").bindparams(id=result.id)

    result = schemas.Vehicle.from_orm(session.execute(sql).one())

    assert result.id is not None
    assert result.name == TEST_VEHICLE.name
    assert result.year_of_manufacture == TEST_VEHICLE.year_of_manufacture
    assert result.body == TEST_VEHICLE.body
    assert result.ready_to_drive == TEST_VEHICLE.ready_to_drive


@pytest.mark.usefixtures("example_data")
def test_get(session: Session):
    """
    Given: A database session with data for multiple vehicles
    When: Retrieving a vehicle by its ID using the Repository
    Then: The corresponding vehicle should be returned
    """
    result = CRUDRepository(models.Vehicle).get(session, id=1)

    assert result.id is not None
    assert result.name == I30.name
    assert result.year_of_manufacture == I30.year_of_manufacture
    assert result.body == I30.body
    assert result.ready_to_drive == I30.ready_to_drive


@pytest.mark.usefixtures("example_data")
def test_get_all(session: Session):
    """
    Given: A database session with data for multiple vehicles
    When: Retrieving all vehicles using the Repository
    Then: The corresponding vehicles should be returned in a list
    """
    result = CRUDRepository(models.Vehicle).get_all(session)

    assert len(result) == 2
    assert isinstance(result, list)


@pytest.mark.usefixtures("example_data")
def test_update(session: Session):
    """
    Given: A database session with data for multiple vehicles
    When: Updating a vehicle by its ID using the Repository
    Then: The corresponding vehicle should be updated
    """
    to_update = CRUDRepository(models.Vehicle).get(session=session, id=1)

    CRUDRepository(models.Vehicle).update(
        session,
        to_update=to_update,
        update_with=schemas.VehicleUpdate(**TEST_VEHICLE.dict()),
    )

    sql = text("SELECT * FROM vehicle WHERE id=:id").bindparams(id=1)
    result = schemas.VehicleInDB.from_orm(session.execute(sql).one())

    assert result.id is not None
    assert result.name == TEST_VEHICLE.name
    assert result.year_of_manufacture == TEST_VEHICLE.year_of_manufacture
    assert result.body == TEST_VEHICLE.body
    assert result.ready_to_drive == TEST_VEHICLE.ready_to_drive


@pytest.mark.usefixtures("example_data")
def test_delete(session: Session):
    """
    Given: A database session with data for multiple vehicles
    When: Deleting a vehicle by its ID using the Repository
    Then: The corresponding vehicle should be deleted
    """
    expected = CRUDRepository(models.Vehicle).get(session=session, id=1)

    CRUDRepository(models.Vehicle).remove(session, id=expected.id)

    sql = text("SELECT * FROM vehicle WHERE id=:id").bindparams(id=1)

    assert not session.execute(sql).first()
