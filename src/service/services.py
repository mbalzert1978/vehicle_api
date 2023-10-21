"""Services module."""
# ruff: noqa: A002
from typing import TypeVar

from src.core.error import HTTPError
from src.core.session import AbstractSession
from src.crud import (
    AbstractRepository,
    CreateSchemaType,
    ModelType,
    UpdateSchemaType,
)

UNPROCESSABLE = 'unprocessable value, not a'
T = TypeVar('T')


def create(
    session: AbstractSession,
    repository: AbstractRepository,
    to_create: CreateSchemaType,
) -> ModelType:
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


def get(
    session: AbstractSession,
    repository: AbstractRepository,
    id: int,
    default: T | None = None,
) -> ModelType:
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
    raise HTTPError(status_code=404, detail='Vehicle not found.')


def list(  # noqa: A001
    session: AbstractSession,
    repository: AbstractRepository,
    filter_by: dict | None = None,
) -> list[ModelType]:
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
    return repository.list(session, filter_by=filter_by)


def update(
    session: AbstractSession,
    repository: AbstractRepository,
    id: int,
    update_with: UpdateSchemaType,
) -> ModelType:
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
        raise HTTPError(status_code=404, detail='Vehicle not found.')
    return repository.update(
        session=session, to_update=to_update, data=update_with
    )


def delete(
    session: AbstractSession, repository: AbstractRepository, id: int
) -> None:
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
    raise HTTPError(status_code=404, detail='Vehicle not found.')
