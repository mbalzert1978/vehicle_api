"""FastAPI vehicles module."""

import operator
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import Connection

from app.database import get_connection
from app.utils.utils import utc_now
from app.vehicles import schemas
from app.vehicles.services import (
    delete_vehicle,
    get_vehicles,
    insert_vehicle,
    update_vehicle,
)

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

FILTER_ON = "filter by %s, optional."


@router.get("/")
def get_all(
    *,
    connection: Annotated[Connection, Depends(get_connection)],
    name: Annotated[
        str | None,
        Query(description=FILTER_ON % "name", examples=["Audi"]),
    ] = None,
    manufacturing_year: Annotated[
        int | None,
        Query(
            le=utc_now().year,
            examples=[2020],
            description=FILTER_ON % "manufacturing year.",
        ),
    ] = None,
    is_driveable: Annotated[
        bool | None,
        Query(
            description=FILTER_ON % "is drivable.",
            examples=[True],
        ),
    ] = None,
) -> schemas.DataMany[schemas.VehicleFromDatabase]:
    """
    List all vehicles.

    Filters can be applied to refine results based on name, manufacturing year, and readiness for driving.
    """
    filter_on = schemas.FilterVehicle(
        name=name, manufacturing_year=manufacturing_year, is_drivable=is_driveable
    )
    vehicles = get_vehicles(connection, filter_on.model_dump(exclude_none=True))
    return schemas.DataMany(
        data=[
            schemas.VehicleFromDatabase.model_validate(vehicle) for vehicle in vehicles
        ]
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def insert(
    *,
    connection: Annotated[Connection, Depends(get_connection)],
    to_create: schemas.CreateVehicle,
) -> schemas.DataOne[schemas.VehicleFromDatabase]:
    r"""
    Create a new vehicle.

    Args:
    ----
    name: The name of the vehicle.\
    year_of_manufacture: The year of manufacture for the vehicle.\
    body: Additional information about the vehicle in the form of a dictionary.
    Defaults to None.\
    ready_to_drive: A boolean flag indicating whether the vehicle is ready to drive.
    Defaults to False.
    """
    result = insert_vehicle(connection, to_create)
    return schemas.DataOne(schemas.VehicleFromDatabase.model_validate(result))


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update(
    *,
    connection: Annotated[Connection, Depends(get_connection)],
    id: uuid.UUID,
    update_with: schemas.UpdateVehicle,
) -> None:
    r"""
    Update a vehicle.

    Args:
    ----
    id: The ID of the vehicle to update.\
    update_with: An instance of `schemas.VehicleUpdate` with updated information.
    """
    if not get_vehicles(connection, dict(id=id)):
        raise HTTPException(status_code=404, detail="Vehicle not found.")
    update_vehicle(connection, id, update_with)


@router.get("/{id}")
def get(
    *,
    connection: Annotated[Connection, Depends(get_connection)],
    id: uuid.UUID,
) -> schemas.DataOne[schemas.VehicleFromDatabase]:
    """
    Get a vehicle by ID.

    Args:
    ----
    id: The ID of the vehicle to retrieve.
    """
    if not (vehicle := get_vehicles(connection, dict(id=id))):
        raise HTTPException(status_code=404, detail="Vehicle not found.")
    return schemas.DataOne(
        schemas.VehicleFromDatabase.model_validate(operator.getitem(vehicle, 0))
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    *,
    connection: Annotated[Connection, Depends(get_connection)],
    id: uuid.UUID,
) -> None:
    """
    Delete an vehicle by ID.

    Args:
    ----
    id: The ID of the vehicle to delete.
    """
    if not get_vehicles(connection, dict(id=id)):
        raise HTTPException(status_code=404, detail="Vehicle not found.")
    delete_vehicle(connection, id)
