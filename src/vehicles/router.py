"""FastAPI vehicles module."""

import uuid
from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncConnection

from src.database import get_connection
from src.utils.utils import utc_now
from src.vehicles import schemas
from src.vehicles.constants import Tag
from src.vehicles.service import delete_vehicle, get_vehicles, insert_vehicle, update_vehicle

tags: list[str | Enum] = [Tag.VEHICLES]

router = APIRouter(prefix=Tag.VEHICLES, tags=tags)

FILTER_ON = "filter by %s, optional."


@router.get("/")
async def get_all(
    *,
    connection: Annotated[AsyncConnection, Depends(get_connection)],
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
            description=FILTER_ON % "is driveable.",
            examples=[True],
        ),
    ] = None,
) -> schemas.ListResponse[schemas.VehicleFromDatabase]:
    """
    List all vehicles.

    Filters can be applied to refine results based on name, manufacturing year, and readiness for driving.
    """
    filter_on = schemas.FilterVehicle(name=name, manufacturing_year=manufacturing_year, is_driveable=is_driveable)
    vehicles = await get_vehicles(connection, filter_on.model_dump(exclude_none=True))
    return schemas.ListResponse(data=[schemas.VehicleFromDatabase.model_validate(vehicle) for vehicle in vehicles])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def insert(
    *,
    connection: Annotated[AsyncConnection, Depends(get_connection)],
    to_create: schemas.CreateVehicle,
) -> schemas.VehicleFromDatabase:
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
    result = await insert_vehicle(connection, to_create)
    return schemas.VehicleFromDatabase.model_validate(result)


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(
    *,
    connection: Annotated[AsyncConnection, Depends(get_connection)],
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
    if not await get_vehicles(connection, dict(id=id)):
        raise HTTPException(status_code=404, detail="Vehicle not found.")
    await update_vehicle(connection, id, update_with)


@router.get("/{id}")
async def get(
    *,
    connection: Annotated[AsyncConnection, Depends(get_connection)],
    id: uuid.UUID,
) -> schemas.VehicleFromDatabase:
    """
    Get a vehicle by ID.

    Args:
    ----
    id: The ID of the vehicle to retrieve.
    """
    if not (vehicle := await get_vehicles(connection, dict(id=id))):
        raise HTTPException(status_code=404, detail="Vehicle not found.")
    return schemas.VehicleFromDatabase.model_validate(vehicle)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    *,
    connection: Annotated[AsyncConnection, Depends(get_connection)],
    id: uuid.UUID,
) -> None:
    """
    Delete an vehicle by ID.

    Args:
    ----
    id: The ID of the vehicle to delete.
    """
    if not await get_vehicles(connection, dict(id=id)):
        raise HTTPException(status_code=404, detail="Vehicle not found.")
    await delete_vehicle(connection, id)
