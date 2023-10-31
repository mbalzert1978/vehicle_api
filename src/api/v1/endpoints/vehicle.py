"""FastAPI vehicles module."""
# mypy: disable-error-code="arg-type"
# ruff: noqa: B008
import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.core.error import HTTPError
from src.core.session import SESSION_LOCAL, AbstractSession
from src.crud import REPOSITORY_LOCAL, AbstractRepository
from src.model.vehicle import Vehicle
from src.schemas import vehicle as schemas
from src.service import services

router = APIRouter(prefix="/vehicle", tags=["vehicle"])

log = logging.getLogger(__name__)

UNCAUGHT = "Uncaught exception"
FILTER_ON = "filter by {criterion}, optional."


@router.get("/", response_model=list[schemas.Vehicle])
def list_vehicle(
    *,
    session: AbstractSession = Depends(SESSION_LOCAL),
    repository: AbstractRepository = Depends(REPOSITORY_LOCAL(Vehicle)),
    name: str
    | None = Query(
        default=None,
        description=FILTER_ON.format(criterion="vehicle name"),
        examples=["Audi"],
    ),
    year_of_manufacture: int
    | None = Query(
        default=None,
        ge=2000,
        le=datetime.datetime.now(tz=datetime.UTC).date().year,
        examples=[2020],
        description=FILTER_ON.format(criterion="year of manufacture"),
    ),
    ready_to_drive: bool
    | None = Query(
        default=None,
        description=FILTER_ON.format(criterion="ready to drive"),
        examples=[True],
    ),
) -> list[schemas.Vehicle]:
    """
    List all vehicles.

    Filters can be applied to refine results based on name, manufacturing year, and readiness for driving.
    """
    try:
        with session as db:
            vehicles: list[Vehicle] = services.list(
                db,
                repository,
                filter_by={
                    "name": name,
                    "year_of_manufacture": year_of_manufacture,
                    "ready_to_drive": ready_to_drive,
                },
            )
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
    else:
        return [schemas.Vehicle.model_validate(vehicle) for vehicle in vehicles]


@router.post("/", response_model=schemas.Vehicle)
def create_vehicle(
    *,
    session: AbstractSession = Depends(SESSION_LOCAL),
    repository: AbstractRepository = Depends(REPOSITORY_LOCAL(Vehicle)),
    to_create: schemas.VehicleCreate,
) -> schemas.Vehicle:
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
    try:
        with session as db:
            vehicle: Vehicle = services.create(
                db,
                repository,
                to_create=to_create,
            )
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
    else:
        return schemas.Vehicle.model_validate(vehicle)


@router.put("/{id}", response_model=schemas.Vehicle)
def update_vehicle(
    *,
    session: AbstractSession = Depends(SESSION_LOCAL),
    repository: AbstractRepository = Depends(REPOSITORY_LOCAL(Vehicle)),
    id: int,  # noqa: A002
    update_with: schemas.VehicleUpdate,
) -> schemas.Vehicle:
    r"""
    Update a vehicle.

    Args:
    ----
    id: The ID of the vehicle to update.\
    update_with: An instance of `schemas.VehicleUpdate` with updated information.
    """
    try:
        with session as db:
            vehicle: Vehicle = services.update(db, repository, id, update_with)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
    else:
        return schemas.Vehicle.model_validate(vehicle)


@router.get("/{id}", response_model=schemas.Vehicle)
def get_vehicle(
    *,
    session: AbstractSession = Depends(SESSION_LOCAL),
    repository: AbstractRepository = Depends(REPOSITORY_LOCAL(Vehicle)),
    id: int,  # noqa: A002
) -> schemas.Vehicle:
    """
    Get a vehicle by ID.

    Args:
    ----
    id: The ID of the vehicle to retrieve.
    """
    try:
        with session as db:
            vehicle: Vehicle = services.get(db, repository, id, Vehicle())
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
    else:
        return schemas.Vehicle.model_validate(vehicle)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    *,
    session: AbstractSession = Depends(SESSION_LOCAL),
    repository: AbstractRepository = Depends(REPOSITORY_LOCAL(Vehicle)),
    id: int,  # noqa: A002
) -> None:
    """
    Delete an vehicle by ID.

    Args:
    ----
    id: The ID of the vehicle to delete.
    """
    try:
        with session as db:
            services.delete(db, repository, id)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
