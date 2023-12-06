"""Services module."""
from src.core.error import HTTPError
from src.crud import AbstractRepository

UNPROCESSABLE = "unprocessable value, not a"


def create[ModelType, CreateSchemaType](repository: AbstractRepository, to_create: CreateSchemaType) -> ModelType:
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
    return repository.create(to_create=to_create)


def get[ModelType, U](repository: AbstractRepository, id: int, default: U | None = None) -> ModelType | U:
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
    if vehicle := repository.get(id=id, default=default):
        return vehicle
    raise HTTPError(status_code=404, detail="Vehicle not found.")


def list[ModelType](repository: AbstractRepository, filter_by: dict | None = None) -> list[ModelType]:
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
    return repository.list(filter_by=_remove_none_values(filter_by or {}))


def _remove_none_values(dictionary: dict) -> dict:
    return {k: v for k, v in dictionary.items() if v is not None}


def update[
    ModelType,
    UpdateSchemaType,
](repository: AbstractRepository, id: int, update_with: UpdateSchemaType) -> ModelType:
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
    if not (to_update := repository.get(id=id)):
        raise HTTPError(status_code=404, detail="Vehicle not found.")
    return repository.update(to_update=to_update, data=update_with)


def delete(repository: AbstractRepository, id: int) -> None:
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
    if repository.delete(id=id):
        return
    raise HTTPError(status_code=404, detail="Vehicle not found.")
