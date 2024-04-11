"""FastAPI vehicles module."""

import datetime
from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Query, status

from vehicle_api import crud
from vehicle_api.api.dependecies.database import get_repository
from vehicle_api.model.vehicle import Vehicle
from vehicle_api.schemas import vehicle as schemas
from vehicle_api.schemas.data_response import ListResponse, Response
from vehicle_api.service import services

router = APIRouter()


FILTER_ON = "filter by %(criterion)s, optional."


@router.get("/")
def list_vehicle(
    *,
    repository: Annotated[crud.AbstractRepository, Depends(get_repository(crud.SQLAlchemyRepository, Vehicle))],
    name: Annotated[
        str | None,
        Query(
            description=FILTER_ON % dict(criterion="vehicle name"),
            examples=["Audi"],
        ),
    ] = None,
    year_of_manufacture: Annotated[
        int | None,
        Query(
            ge=2000,
            le=datetime.datetime.now(tz=datetime.UTC).date().year,
            examples=[2020],
            description=FILTER_ON % dict(criterion="year of manufacture"),
        ),
    ] = None,
    ready_to_drive: Annotated[
        bool | None,
        Query(
            description=FILTER_ON % dict(criterion="ready to drive"),
            examples=[True],
        ),
    ] = None,
) -> ListResponse[schemas.VehicleFromDatabase]:
    """
    List all vehicles.

    Filters can be applied to refine results based on name, manufacturing year, and readiness for driving.
    """
    vehicles: Sequence[Vehicle] = services.list(
        repository,
        filter_by={
            "name": name,
            "year_of_manufacture": year_of_manufacture,
            "ready_to_drive": ready_to_drive,
        },
    )
    return ListResponse(data=[schemas.VehicleFromDatabase.model_validate(vehicle) for vehicle in vehicles])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vehicle(
    *,
    repository: Annotated[crud.AbstractRepository, Depends(get_repository(crud.SQLAlchemyRepository, Vehicle))],
    to_create: schemas.VehicleForCreate,
) -> Response[int]:
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
    return Response(services.create(repository, to_create))


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_vehicle(
    *,
    repository: Annotated[crud.AbstractRepository, Depends(get_repository(crud.SQLAlchemyRepository, Vehicle))],
    id: int,
    update_with: schemas.VehicleForUpdate,
) -> None:
    r"""
    Update a vehicle.

    Args:
    ----
    id: The ID of the vehicle to update.\
    update_with: An instance of `schemas.VehicleUpdate` with updated information.
    """
    services.update(repository, id, update_with)


@router.get("/{id}")
def get_vehicle(
    *,
    repository: Annotated[crud.AbstractRepository, Depends(get_repository(crud.SQLAlchemyRepository, Vehicle))],
    id: int,
) -> Response[schemas.VehicleFromDatabase]:
    """
    Get a vehicle by ID.

    Args:
    ----
    id: The ID of the vehicle to retrieve.
    """
    return Response(schemas.VehicleFromDatabase.model_validate(services.get(repository, id)))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    *,
    repository: Annotated[crud.AbstractRepository, Depends(get_repository(crud.SQLAlchemyRepository, Vehicle))],
    id: int,
) -> None:
    """
    Delete an vehicle by ID.

    Args:
    ----
    id: The ID of the vehicle to delete.
    """
    services.delete(repository, id)
