"""Services module."""
# ruff: noqa: A002
from enum import Enum
from typing import TypeVar

from src.core.error import HTTPError
from src.core.session import AbstractSession
from src.crud import AbstractRepository, CreateSchemaType, ModelType, UpdateSchemaType

UNPROCESSABLE = "unprocessable value, not a"
T = TypeVar("T")


class FilterBy(str, Enum):

    """Filter by Enum."""

    NAME = "name"
    YEAR_OF_MANUFACTURE = "year_of_manufacture"
    READY_TO_DRIVE = "ready_to_drive"


def create(session: AbstractSession, repository: AbstractRepository, to_create: CreateSchemaType) -> ModelType:
    """
    Create a new vehicle.

    Args:
    ----
    session: An Session object.
    repository: An AbstractRepository object.
    to_create: A object to create.

    Returns:
    -------
    A object representing the created vehicle.

    Raises:
    ------
    HTTPError: If the vehicle already exists.
    """
    return repository.create(session=session, to_create=to_create)


def get(session: AbstractSession, repository: AbstractRepository, id: int, default: T | None = None) -> ModelType:
    """
    Get a vehicle.

    Args:
    ----
    session: An Session object.
    repository: An AbstractRepository object.
    id: The id of the vehicle.
    default: The default value to return if the vehicle does not exist.

    Returns:
    -------
    A object representing the vehicle.

    Raises:
    ------
    HTTPError: If the vehicle does not exist.
    """
    if vehicle := repository.get(session=session, id=id, default=default):
        return vehicle
    raise HTTPError(status_code=404, detail="Vehicle not found.")


def list_all(session: AbstractSession, repository: AbstractRepository) -> list[ModelType]:
    """
    List all vehicles.

    Args:
    ----
    session: An Session object.
    repository: A AbstractRepository object.
    offset: The offset of the data.
    limit: The limit of the displayed data.

    Returns:
    -------
    A list of `Vehicle` objects representing the vehicles.

    """
    return repository.list(session)


def filter_by(session: AbstractSession, repository: AbstractRepository, filter_by: FilterBy,
              value: str) -> list[ModelType]:
    """
    Filter vehicles by a given value.

    Args:
    ----
    session: An Session object.
    repository: An AbstractRepository object.
    filter_by: The filter by to apply.
    value: The value to filter by.

    Returns:
    -------
    A list of `Vehicle` objects representing the vehicles.

    Raises:
    ------
    HTTPError: If the filter by is invalid.
    """
    match filter_by:
        case FilterBy.NAME:
            return repository.list(session=session, filter_by={FilterBy.NAME: value})
        case FilterBy.YEAR_OF_MANUFACTURE:
            parsed = _parse_int(value)
            return repository.list(session=session, filter_by={FilterBy.YEAR_OF_MANUFACTURE: parsed})
        case FilterBy.READY_TO_DRIVE:
            parsed = _parse_bool(value)
            return repository.list(session=session, filter_by={FilterBy.READY_TO_DRIVE: parsed})


def _parse_int(value: str) -> int:
    """Parse a string to an integer."""
    try:
        parsed = int(value)
    except (ValueError, TypeError) as e:
        raise HTTPError(status_code=422, detail=f"{UNPROCESSABLE} integer.") from e
    else:
        return parsed


def _parse_bool(value: str) -> bool:
    """Convert a string to a boolean."""
    return value.lower() in {"yes", "true", "t", "1"}


def update(session: AbstractSession, repository: AbstractRepository, id: int,
           update_with: UpdateSchemaType) -> ModelType:
    """
    Update a vehicle by ID.

    Args:
    ----
    session: An Session object.
    id: The ID of the vehicle to update.
    repository: A AbstractRepository object.
    update_with: The data to update the vehicle with.

    Returns:
    -------
    A `Vehicle` object representing the updated vehicle.

    Raises:
    ------
    HTTPError: If the vehicle with the specified ID is not found.
    """
    if not (to_update := repository.get(session=session, id=id)):
        raise HTTPError(status_code=404, detail="Vehicle not found.")
    return repository.update(session=session, to_update=to_update, data=update_with)


def delete(session: AbstractSession, repository: AbstractRepository, id: int) -> None:
    """
    Delete a vehicle by ID.

    Args:
    ----
    session: An Session object.
    repository: A AbstractRepository object.
    id: The ID of the vehicle to delete.

    Raises:
    ------
    HTTPError: If the vehicle with the specified ID is not found.
    """
    if repository.delete(session=session, id=id):
        return
    raise HTTPError(status_code=404, detail="Vehicle not found.")
