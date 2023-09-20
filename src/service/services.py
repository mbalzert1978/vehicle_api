"""Services module."""
from enum import Enum

from src.core.error import HTTPError
from src.core.session import Session
from src.crud import AbstractRepository
from src.schemas import vehicle as schemas

UNPROCESSABLE = "unprocessable value, not a"


class FilterBy(str, Enum):

    """Filter by Enum."""

    NAME = "name"
    YEAR_OF_MANUFACTURE = "year_of_manufacture"
    READY_TO_DRIVE = "ready_to_drive"


def create(session: Session, repository: AbstractRepository, name: str, year_of_manufacture: int, body: dict | None, *,
           ready_to_drive: bool) -> schemas.Vehicle:
    """
    Create a new vehicle.

    Args:
    ----
    session: An Session object.
    repository: An AbstractRepository object.
    name: The name of the vehicle.
    year_of_manufacture: The year of manufacture of the vehicle.
    body: Additional details about the vehicle in the form of a dictionary.
    Defaults to an empty dictionary if None.
    ready_to_drive: A boolean indicating whether the vehicle is ready to drive.

    Returns:
    -------
    A `Vehicle` object representing the created vehicle.
    """
    vehicle = repository.create(
        session=session,
        to_create=schemas.VehicleCreate(name=name,
                                        year_of_manufacture=year_of_manufacture,
                                        body=body or {},
                                        ready_to_drive=ready_to_drive),
    )
    return schemas.Vehicle.from_orm(vehicle)


def get(session: Session, repository: AbstractRepository, id: int) -> schemas.Vehicle:  # noqa: A002
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
        return schemas.Vehicle.from_orm(vehicle)
    raise HTTPError(status_code=404, detail="Vehicle not found.")


def list_all(session: Session, repository: AbstractRepository) -> list[schemas.Vehicle]:
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
    return [schemas.Vehicle.from_orm(vehicle) for vehicle in repository.list(session)]


def filter_by(session: Session, repository: AbstractRepository, filter_by: FilterBy,
              value: str) -> list[schemas.Vehicle]:
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
            vehicles = repository.list(session=session, filter_by={FilterBy.NAME: value})
        case FilterBy.YEAR_OF_MANUFACTURE:
            parsed = _parse_int(value)
            vehicles = repository.list(session=session, filter_by={FilterBy.YEAR_OF_MANUFACTURE: parsed})
        case FilterBy.READY_TO_DRIVE:
            parsed = _parse_bool(value)
            vehicles = repository.list(session=session, filter_by={FilterBy.READY_TO_DRIVE: parsed})
    return [schemas.Vehicle.from_orm(vehicle) for vehicle in vehicles]

def _parse_int(value:str) -> int:
    """Parse a string to an integer."""
    try:
        parsed = int(value)
    except ValueError as e:
        raise HTTPError(status_code=422, detail=f"{UNPROCESSABLE} integer.") from e
    else:
        return parsed


def _parse_bool(value: str) -> bool:
    """Convert a string to a boolean."""
    return value.lower() in {"yes", "true", "t", "1"}


def update(
        session: Session,
        repository: AbstractRepository,
        id: int,  # noqa: A002
        update_with: schemas.VehicleUpdate) -> schemas.Vehicle:
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
    return schemas.Vehicle.from_orm(repository.update(session=session, to_update=to_update, data=update_with))


def delete(session: Session, repository: AbstractRepository, id: int) -> None:  # noqa: A002
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
