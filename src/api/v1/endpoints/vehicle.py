"""FastAPI vehicles module."""
# mypy: disable-error-code="arg-type"
# ruff: noqa: B008
import logging

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import session_factory
from src.core.error import HTTPError
from src.core.session import Session
from src.crud import REPOSITORY_GETTER, AbstractRepository
from src.schemas import vehicle as schemas
from src.service import services

router = APIRouter(prefix="/vehicle", tags=["vehicle"])

log = logging.getLogger(__name__)

UNCAUGHT = "Uncaught exception"


@router.get("/", response_model=list[schemas.Vehicle])
def list_vehicle(
    *,
    session: Session = Depends(session_factory),
    repository: type[AbstractRepository] = Depends(REPOSITORY_GETTER),
) -> list[schemas.Vehicle]:
    """List all vehicles."""
    try:
        with session as db:
            return services.list_all(db, repository)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.get("/{filter_by}/{value}", response_model=list[schemas.Vehicle])
def filter_vehicle(
    *,
    filter_by: services.FilterBy,
    value: str,
    session: Session = Depends(session_factory),
    repository: type[AbstractRepository] = Depends(REPOSITORY_GETTER),
) -> list[schemas.Vehicle]:
    """Filter vehicles based on a given criterion."""
    try:
        with session as db:
            return services.filter_by(db, repository, filter_by, value)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.post("/", response_model=schemas.Vehicle)
def create_vehicle(  # noqa: D417
    *,
    session: Session = Depends(session_factory),
    repository: type[AbstractRepository] = Depends(REPOSITORY_GETTER),
    name: str,
    year_of_manufacture: int,
    body: dict | None = None,
    ready_to_drive: bool = False,
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
            return services.create(
                db,
                repository,
                name,
                year_of_manufacture,
                body,
                ready_to_drive=ready_to_drive,
            )
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.put("/{id}", response_model=schemas.Vehicle)
def update_vehicle(  # noqa: D417
    *,
    session: Session = Depends(session_factory),
    repository: type[AbstractRepository] = Depends(REPOSITORY_GETTER),
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
            return services.update(db, repository, id, update_with)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.get("/{id}", response_model=schemas.Vehicle)
def get_vehicle(  # noqa: D417
        *,
        session: Session = Depends(session_factory),
        repository: type[AbstractRepository] = Depends(REPOSITORY_GETTER),
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
            return services.get(db, repository, id)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(  # noqa: D417
        *,
        session: Session = Depends(session_factory),
        repository: type[AbstractRepository] = Depends(REPOSITORY_GETTER),
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
