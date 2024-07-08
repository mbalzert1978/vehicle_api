import json

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from src.database import execute
from src.vehicles.schemas import CreateVehicle, UpdateVehicle, VehicleFromDatabase
from src.vehicles.services import delete_vehicle, get_vehicles, insert_vehicle, update_vehicle


@pytest.mark.asyncio()
async def test_insert_vehicle_when_called_with_create_vehicle_obj_should_insert_data_into_vehicles_table(
    connection: AsyncConnection,
) -> None:
    """
    Given: A empty database session
    When: Creating a new vehicle using the service insert_vehicle
    Then: The vehicle should be added to the database and the
        vehicle should be returned with a valid id.
    """
    to_create = CreateVehicle(name="Test Vehicle", manufacturing_year=2020, is_drivable=True, body={"type": "car"})
    result = await insert_vehicle(connection, to_create)

    query = text("SELECT * FROM vehicles WHERE id = :id").bindparams(id=result["id"])
    raw_sql = await execute(connection, query)

    assert VehicleFromDatabase.model_validate(result) == VehicleFromDatabase.model_validate(raw_sql.mappings().one())


@pytest.mark.asyncio()
@pytest.mark.usefixtures("example_data")
async def test_get_vehicles_when_called_should_return_all_vehicles(connection: AsyncConnection) -> None:
    """
    Given: A database with vehicles
    When: Getting all vehicles using the service get_vehicles
    Then: All vehicles should be returned.
    """
    result = await get_vehicles(connection, {})

    assert result[0].name == "Q7"
    assert result[-1].name == "I30"


@pytest.mark.asyncio()
@pytest.mark.usefixtures("example_data")
async def test_delete_vehicle_when_called_with_uuid_should_delete_data_in_vehicles_table(
    connection: AsyncConnection,
) -> None:
    """
    Given: A database with a vehicle
    When: Delete vehicle service is called with the uuid of the vehicle
    Then: The vehicle should be deleted from the database.
    """
    [q7] = await get_vehicles(connection, dict(name="Q7"))

    await delete_vehicle(connection, id := q7["id"])

    query = text("SELECT * FROM vehicles WHERE id = :id").bindparams(id=id)
    raw_sql = await execute(connection, query)

    assert raw_sql.mappings().one_or_none() is None


@pytest.mark.asyncio()
@pytest.mark.usefixtures("example_data")
async def test_update_vehicle_when_called_with_uuid_should_update_data_in_vehicles_table(
    connection: AsyncConnection,
) -> None:
    """
    Given: A database with a vehicle
    When: update vehicle service is called with the uuid of the vehicle
    Then: The vehicle should be updated in the database.
    """
    [i30] = await get_vehicles(connection, dict(name="I30"))

    update_with = UpdateVehicle(name="updated_name")

    await update_vehicle(connection, id := i30["id"], update_with)

    query = text("SELECT * FROM vehicles WHERE id = :id").bindparams(id=id)
    raw_sql = await execute(connection, query)
    updated = raw_sql.mappings().one()

    assert updated.name == "updated_name"
    assert updated.manufacturing_year == i30["manufacturing_year"]
    assert updated.is_drivable == i30["is_drivable"]
    assert json.loads(updated.body) == i30["body"]
    assert updated.created_at == i30["created_at"].isoformat(" ")
    assert updated.updated_at is not None
