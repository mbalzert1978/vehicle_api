"""FastAPI vehicles module."""

# mypy: disable-error-code="arg-type"
# ruff: noqa: B008
import datetime
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src import crud
from src.api.dependecies.database import get_repository
from src.model.vehicle import Vehicle
from src.schemas import vehicle as schemas
from src.schemas.data_response import ListResponse, Response
from src.service import services

router = APIRouter()

log = logging.getLogger(__name__)

UNCAUGHT = "Uncaught exception"
FILTER_ON = "filter by {criterion}, optional."


@router.get("/")
def list_vehicle(
    *,
    repository: Annotated[crud.AbstractRepository, Depends(get_repository(crud.SQLAlchemyRepository, Vehicle))],
    name: str | None = Query(
        default=None,
        description=FILTER_ON.format(criterion="vehicle name"),
        examples=["Audi"],
    ),
    year_of_manufacture: int | None = Query(
        default=None,
        ge=2000,
        le=datetime.datetime.now(tz=datetime.UTC).date().year,
        examples=[2020],
        description=FILTER_ON.format(criterion="year of manufacture"),
    ),
    ready_to_drive: bool | None = Query(
        default=None,
        description=FILTER_ON.format(criterion="ready to drive"),
        examples=[True],
    ),
) -> ListResponse[list[schemas.Vehicle]]:
    """
    List all vehicles.

    Filters can be applied to refine results based on name, manufacturing year, and readiness for driving.
    """

    vehicles: list[Vehicle] = services.list(
        repository,
        filter_by={
            "name": name,
            "year_of_manufacture": year_of_manufacture,
            "ready_to_drive": ready_to_drive,
        },
    )
    return ListResponse(data=[schemas.Vehicle.model_validate(vehicle) for vehicle in vehicles])


@router.post("/")
def create_vehicle(
    *,
    repository: Annotated[crud.AbstractRepository, Depends(get_repository(crud.SQLAlchemyRepository, Vehicle))],
    to_create: schemas.VehicleCreate,
) -> Response[schemas.Vehicle]:
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
    return Response(schemas.Vehicle.model_validate(services.create(repository, to_create=to_create)))


@router.put("/{id}")
def update_vehicle(
    *,
    repository: Annotated[crud.AbstractRepository, Depends(get_repository(crud.SQLAlchemyRepository, Vehicle))],
    id: int,
    update_with: schemas.VehicleUpdate,
) -> Response[schemas.Vehicle]:
    r"""
    Update a vehicle.

    Args:
    ----
    id: The ID of the vehicle to update.\
    update_with: An instance of `schemas.VehicleUpdate` with updated information.
    """
    return Response(schemas.Vehicle.model_validate(services.update(repository, id, update_with)))


@router.get("/{id}")
def get_vehicle(
    *,
    repository: Annotated[crud.AbstractRepository, Depends(get_repository(crud.SQLAlchemyRepository, Vehicle))],
    id: int,
) -> Response[schemas.Vehicle]:
    """
    Get a vehicle by ID.

    Args:
    ----
    id: The ID of the vehicle to retrieve.
    """
    return Response(schemas.Vehicle.model_validate(services.get(repository, id)))


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
