# type: ignore  # noqa: PGH003

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

import src.model.vehicle as model
import src.schemas.vehicle as schemas
from src.crud.sqlalchemy_repo import SQLAlchemyRepository
from src.monads.result import Ok
from tests.data import I30, TEST_VEHICLE


def test_create(session: Session):
    """
    Given: A empty database session
    When: Creating a new vehicle using the Repository
    Then: The vehicle should be added to the database and the
        vehicle should be returned with a valid id.
    """
    match SQLAlchemyRepository(model.Vehicle).create(session, to_create=TEST_VEHICLE):
        case Ok(result):
            sql = text("SELECT * FROM vehicle WHERE id=:id").bindparams(id=result.id)

    result = schemas.Vehicle.model_validate(session.execute(sql).one())

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
    Then: The corresponding vehicle should be returned.
    """
    match SQLAlchemyRepository(model.Vehicle).get(session, id=1):
        case Ok(result):
            assert result.id is not None
            assert result.name == I30.name
            assert result.year_of_manufacture == I30.year_of_manufacture
            assert result.body == I30.body
            assert result.ready_to_drive == I30.ready_to_drive
        case _:
            pytest.fail("Not a correct result.")


@pytest.mark.usefixtures("example_data")
def test_list(session: Session):
    """
    Given: A database session with data for multiple vehicles
    When: Retrieving all vehicles using the Repository
    Then: The corresponding vehicles should be returned in a list.
    """
    match SQLAlchemyRepository(model.Vehicle).list(session):
        case Ok(result):
            assert len(result) == 2
            assert isinstance(result, list)
        case _:
            pytest.fail("Not a correct result.")


@pytest.mark.usefixtures("example_data")
def test_update(session: Session):
    """
    Given: A database session with data for multiple vehicles
    When: Updating a vehicle by its ID using the Repository
    Then: The corresponding vehicle should be updated.
    """
    match SQLAlchemyRepository(model.Vehicle).get(session=session, id=1):
        case Ok(to_update):
            SQLAlchemyRepository(model.Vehicle).update(
                session,
                to_update=to_update,
                data=schemas.VehicleUpdate(**TEST_VEHICLE.model_dump()),
            )

            sql = text("SELECT * FROM vehicle WHERE id=:id").bindparams(id=1)
            result = schemas.VehicleInDB.model_validate(session.execute(sql).one())

            assert result.id is not None
            assert result.name == TEST_VEHICLE.name
            assert result.year_of_manufacture == TEST_VEHICLE.year_of_manufacture
            assert result.body == TEST_VEHICLE.body
            assert result.ready_to_drive == TEST_VEHICLE.ready_to_drive
        case _:
            pytest.fail("Not a correct result.")


@pytest.mark.usefixtures("example_data")
def test_delete(session: Session):
    """
    Given: A database session with data for multiple vehicles
    When: Deleting a vehicle by its ID using the Repository
    Then: The corresponding vehicle should be deleted.
    """
    match SQLAlchemyRepository(model.Vehicle).get(session=session, id=1):
        case Ok(expected):
            SQLAlchemyRepository(model.Vehicle).delete(session, id=expected.id)

            sql = text("SELECT * FROM vehicle WHERE id=:id").bindparams(id=1)

            assert not session.execute(sql).first()
        case _:
            pytest.fail("Not a correct result.")
