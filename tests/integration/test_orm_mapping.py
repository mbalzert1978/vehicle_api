import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, text
from sqlalchemy.orm import Session

import src.model.vehicle as model
from src.vehicles import schemas
from tests.data import I30, TEST_VEHICLE


def test_create_vehicle(session: Session) -> None:
    """
    Given: A database session
    When: Creating a new vehicle
    Then: The vehicle should be added to the database.
    """
    expected = model.Vehicle(**I30.model_dump())

    session.add(expected)
    session.commit()

    sql = text("SELECT * FROM vehicle WHERE id=:id").bindparams(id=1)
    result = schemas.VehicleFromDatabase.model_validate(session.execute(sql).one())

    assert result.name == expected.name
    assert result.year_of_manufacture == expected.year_of_manufacture
    assert result.body == expected.body
    assert result.ready_to_drive == expected.ready_to_drive


@pytest.mark.usefixtures("example_data")
def test_read_vehicle(session: Session) -> None:
    """
    Given: A database session with a vehicle
    When: Reading the vehicle from the database
    Then: The vehicle data should match the expected values.
    """
    expected = session.execute(select(model.Vehicle)).scalars().first()

    assert expected is not None
    assert expected.name == I30.name
    assert expected.year_of_manufacture == I30.year_of_manufacture
    assert expected.body == I30.body
    assert expected.ready_to_drive == I30.ready_to_drive


@pytest.mark.usefixtures("example_data")
def test_update_vehicle(session: Session) -> None:
    """
    Given: A database session with a vehicle
    When: Updating the vehicle data
    Then: The vehicle data should be updated in the database.
    """
    result = session.execute(select(model.Vehicle)).scalars().first()
    serialized = jsonable_encoder(result)

    expected = TEST_VEHICLE.model_dump(exclude_unset=True)

    for field in serialized:
        if field not in expected:
            continue
        setattr(result, field, expected[field])

    session.add(result)
    session.commit()
    session.refresh(result)

    assert result.name == expected["name"]
    assert result.year_of_manufacture == expected["year_of_manufacture"]
    assert result.body == expected["body"]
    assert result.ready_to_drive == expected["ready_to_drive"]
