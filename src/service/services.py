"""Services module."""
from enum import Enum
from typing import TypeVar

from src.core.error import HTTPError
from src.core.session import AbstractSession
from src.crud import AbstractRepository

T = TypeVar("T")
UNPROCESSABLE = "unprocessable value, not a"


class FilterBy(str, Enum):
    """Filter by Enum."""

    NAME = "name"
    YEAR_OF_MANUFACTURE = "year_of_manufacture"
    READY_TO_DRIVE = "ready_to_drive"


def create(session: AbstractSession, repository: AbstractRepository, to_create: T) -> T:
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


def get(session: AbstractSession, repository: AbstractRepository, id: int) -> T:  # noqa: A002
    """
        Get a vehicle by ID.

    Args:
    ----
    session: An Session object.
    repository: An AbstractRepository object.
    id: The ID of the vehicle to retrieve.

    Returns:
    -------
    A `Vehicle` object representing the retrieved vehicle.

    Raises:
    ------
    HTTPError: If the vehicle with the specified ID is not found.
    """
    if vehicle := repository.get(session=session, id=id):
        return vehicle
    raise HTTPError(status_code=404, detail="Vehicle not found.")


def list_all(session: AbstractSession, repository: AbstractRepository) -> list[T]:
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


def filter_by(session: AbstractSession, repository: AbstractRepository, filter_by: FilterBy, value: str) -> list[T]:
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


def update(session: AbstractSession, repository: AbstractRepository, id: int, update_with: T) -> T:  # noqa: A002
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


def delete(session: AbstractSession, repository: AbstractRepository, id: int) -> None:  # noqa: A002
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
