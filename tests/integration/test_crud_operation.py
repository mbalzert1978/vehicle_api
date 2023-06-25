# type: ignore  # noqa: PGH003

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

import src.model.vehicle as model
import src.schemas.vehicle as schemas
from src.crud.base import CRUDBase

TEST_VEHICLE = schemas.VehicleCreate(
    name="test_car",
    year_of_manufacture=2020,
    body={
        "color": "test_color",
        "kilometer": 10,
        "price": 10_000,
        "vehicle_type": "test_type",
    },
    ready_to_drive=False,
)


def test_create(session: Session):
    """
    Given: A empty database session
    When: Creating a new vehicle using the Repository
    Then: The vehicle should be added to the database and the
        vehicle should be returned with a valid id
    """
    result = CRUDBase(model.Vehicle).create(session, to_create=TEST_VEHICLE)

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
    result = CRUDBase(model.Vehicle).get(session, id=1)

    assert result.id is not None
    assert result.name == "I30"
    assert result.year_of_manufacture == 2017
    assert result.body == {
        "color": "black",
        "kilometer": 10000,
        "price": 15000,
        "vehicle_type": "limusine",
    }
    assert result.ready_to_drive


@pytest.mark.usefixtures("example_data")
def test_get_all(session: Session):
    """
    Given: A database session with data for multiple vehicles
    When: Retrieving all vehicles using the Repository
    Then: The corresponding vehicles should be returned in a list
    """
    result = CRUDBase(model.Vehicle).get_all(session)

    assert result
    assert isinstance(result, list)


@pytest.mark.usefixtures("example_data")
def test_update(session: Session):
    """
    Given: A database session with data for multiple vehicles
    When: Updating a vehicle by its ID using the Repository
    Then: The corresponding vehicle should be updated
    """
    if not (to_update := CRUDBase(model.Vehicle).get(session=session, id=1)):
        pytest.fail("vehicle not in database")

    result = CRUDBase(model.Vehicle).update(
        session,
        to_update=to_update,
        update_with={"name": "new_test_car"},
    )
    sql = text("SELECT * FROM vehicle WHERE id=:id").bindparams(id=1)

    result = schemas.VehicleInDB.from_orm(session.execute(sql).one())

    assert result.id is not None
    assert result.name == "new_test_car"
    assert result.year_of_manufacture == to_update.year_of_manufacture
    assert result.body == to_update.body
    assert result.ready_to_drive == to_update.ready_to_drive


@pytest.mark.usefixtures("example_data")
def test_delete(session: Session):
    """
    Given: A database session with data for multiple vehicles
    When: Deleting a vehicle by its ID using the Repository
    Then: The corresponding vehicle should be deleted
    """
    sql = text("SELECT * FROM vehicle WHERE id=:id").bindparams(id=1)
    expected = schemas.VehicleInDB.from_orm(session.execute(sql).one())

    CRUDBase(model.Vehicle).remove(session, id=expected.id)

    sql = text("SELECT * FROM vehicle WHERE id=:id").bindparams(id=1)

    assert not session.execute(sql).first()
