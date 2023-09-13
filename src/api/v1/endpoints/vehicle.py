"""FastAPI vehicles module."""
# mypy: disable-error-code="arg-type"

import logging

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import session_factory
from src.core.error import HTTPError
from src.core.session import Session
from src.schemas import vehicle as schemas
from src.service import services

router = APIRouter(prefix="/vehicle", tags=["vehicle"])

log = logging.getLogger(__name__)

UNCAUGHT = "Uncaught exception"
OFFSET = 0
LIMIT = 100


@router.get("/", response_model=list[schemas.Vehicle])
def list_vehicle(  # noqa: D417
    *,
    session: Session = Depends(session_factory),  # noqa: B008
) -> list[schemas.Vehicle]:
    r"""
    List all vehicles.

    Args:
    ----
    offset: The offset of the data. Defaults to 0.\
    limit: The limit of the displayed data. Defaults to 100.

    Raises:
    ------
    HTTPException: If an HTTP error occurs during the listing process.

    Returns:
    -------
    A list of `Vehicle` objects representing all the vehicles.
    """
    try:
        with session as db:
            return services.list_all(db)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.get("/{filter_by}/{value}", response_model=list[schemas.Vehicle])
def filter_vehicle(  # noqa: D417
    *,
    filter_by: services.FilterBy,
    value: str,
    session: Session = Depends(session_factory),  # noqa: B008
) -> list[schemas.Vehicle]:
    r"""
    Filter vehicles based on a given criterion.

    Args:
    ----
    filter_by: An instance of services.FilterBy for vehicle filtering criterion.\
    value: The value used for filtering. It can be a string, integer, or boolean.

    Raises:
    ------
    HTTPException: If an HTTP error occurs during the filtering process.

    Returns:
    -------
    A list of `Vehicle` objects matching the filtering criterion.
    """
    try:
        with session as db:
            return services.filter_by(db, filter_by, value)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.post("/", response_model=schemas.Vehicle)
def create_vehicle(  # noqa: D417
    *,
    session: Session = Depends(session_factory),  # noqa: B008,
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

    Raises:
    ------
    HTTPException: If an HTTP error occurs during the creation process.

    Returns:
    -------
    The created `Vehicle` object.
    """
    try:
        with session as db:
            return services.create(
                db,
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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.put("/{id}", response_model=schemas.Vehicle)
def update_vehicle(  # noqa: D417
    *,
    session: Session = Depends(session_factory),  # noqa: B008
    id: int,  # noqa: A002
    update_with: schemas.VehicleUpdate,
) -> schemas.Vehicle:
    r"""
    Update a vehicle.

    Args:
    ----
    id: The ID of the vehicle to update.\
    update_with: An instance of `schemas.VehicleUpdate` with updated information.

    Raises:
    ------
    HTTPException: If an HTTP error occurs during the update process.

    Returns:
    -------
    The updated `Vehicle` object.
    """
    try:
        with session as db:
            return services.update(db, id, update_with)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.get("/{id}", response_model=schemas.Vehicle)
def get_vehicle(  # noqa: D417
    *,
    session: Session = Depends(session_factory),  # noqa: B008
    id: int,  # noqa: A002
) -> schemas.Vehicle:
    """
    Get a vehicle by ID.

    Args:
    ----
    id: The ID of the vehicle to retrieve.

    Raises:
    ------
    HTTPException: If an HTTP error occurs during the retrieval process.

    Returns:
    -------
    The `Vehicle` object with the specified ID.
    """
    try:
        with session as db:
            return services.get(db, id)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(  # noqa: D417
    *,
    session: Session = Depends(session_factory),  # noqa: B008
    id: int,  # noqa: A002
) -> None:
    """
    Delete an vehicle by ID.

    Args:
    ----
    id: The ID of the vehicle to delete.

    Raises:
    ------
    HTTPException: If an HTTP error occurs during the deletion process.
    """
    try:
        with session as db:
            services.delete(db, id)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e
