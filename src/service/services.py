"""Services module."""
# ruff: noqa: A002
from collections.abc import Sequence
from typing import TypeVar

from src.core.error import NotFoundError
from src.core.session import AbstractSession
from src.crud import AbstractRepository, CreateSchemaType, ModelType, UpdateSchemaType
from src.monads.result import Err, Ok, Result

UNPROCESSABLE = "unprocessable value, not a"
T = TypeVar("T")


def create(
    session: AbstractSession,
    repository: AbstractRepository,
    to_create: CreateSchemaType,
) -> Result[ModelType, Exception]:
    """
    Create a new vehicle.

    Args:
    ----
    session: An Session object.
    repository: An AbstractRepository object.
    to_create: A object to create.

    Returns:
    -------
    A result object representing the created vehicle.
    """
    return repository.create(session=session, to_create=to_create)


def get(session: AbstractSession, repository: AbstractRepository, id: int) -> Result[ModelType, Exception]:
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
    return repository.get(session=session, id=id)


def list(  # noqa: A001
    session: AbstractSession,
    repository: AbstractRepository,
    filter_by: dict | None = None,
) -> Result[Sequence[ModelType], Exception]:
    """
    List all vehicles.

    Given filter_by parameter the vehicle will be filtered.

    Args:
    ----
    session: An Session object.
    repository: An AbstractRepository object.
    filter_by: A dict of filter criterions. Defaults to None.

    Returns:
    -------
    returns: A list of `Vehicle` objects.
    """
    return repository.list(session, filter_by=_remove_none_values(filter_by))


def _remove_none_values(dictionary: dict) -> dict:
    return {k: v for k, v in dictionary.items() if v is not None}


def update(
    session: AbstractSession,
    repository: AbstractRepository,
    id: int,
    update_with: UpdateSchemaType,
) -> Result[ModelType, Exception]:
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
    match repository.get(session=session, id=id):
        case Ok(None):
            return Err(NotFoundError(id))
        case Ok(to_update):
            return repository.update(session=session, to_update=to_update, data=update_with)


def delete(session: AbstractSession, repository: AbstractRepository, id: int) -> Result[ModelType, Exception]:
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
    match repository.get(session=session, id=id):
        case Ok(None):
            return Err(NotFoundError(id))
        case Ok(to_delete):
            return repository.delete(session=session, to_delete=to_delete)
