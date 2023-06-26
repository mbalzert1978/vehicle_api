"""Services module."""
from enum import Enum

from sqlalchemy.orm import Session

from src.core.error import HTTPError
from src.crud import repository
from src.model import vehicle as models
from src.schemas import vehicle as schemas

UNPROCESSABLE = "unprocessable value, not a"


class FilterBy(str, Enum):

    """Filter by Enum."""

    NAME = "name"
    YEAR_OF_MANUFACTURE = "year_of_manufacture"
    READY_TO_DRIVE = "ready_to_drive"


def create(
    session: Session,
    name: str,
    year_of_manufacture: int,
    body: dict | None,
    *,
    ready_to_drive: bool,
) -> schemas.Vehicle:
    """
    Create a new vehicle.

    Args:
    ----
    session: An SQLAlchemy Session object.
    name: The name of the vehicle.
    year_of_manufacture: The year of manufacture of the vehicle.
    body: Additional details about the vehicle in the form of a dictionary.
    Defaults to an empty dictionary if None.
    ready_to_drive: A boolean indicating whether the vehicle is ready to drive.

    Returns:
    -------
    A `schemas.Vehicle` object representing the created vehicle.
    """
    vehicle = repository.factory(models.Vehicle).create(
        session=session,
        to_create=schemas.VehicleCreate(
            name=name,
            year_of_manufacture=year_of_manufacture,
            body=body or {},
            ready_to_drive=ready_to_drive,
        ),
    )
    return schemas.Vehicle.from_orm(vehicle)


def get(session: Session, id: int) -> schemas.Vehicle:  # noqa: A002
    """
        Get a vehicle by ID.

    Args:
    ----
    session: An SQLAlchemy Session object.
    id: The ID of the vehicle to retrieve.

    Returns:
    -------
    A `schemas.Vehicle` object representing the retrieved vehicle.

    Raises:
    ------
    HTTPError: If the vehicle with the specified ID is not found.
    """
    if vehicle := repository.factory(models.Vehicle).get(
        session=session,
        id=id,
    ):
        return schemas.Vehicle.from_orm(vehicle)
    raise HTTPError(status_code=404, detail="Vehicle not found.")


def list_all(
    session: Session,
    offset: int,
    limit: int,
) -> list[schemas.Vehicle]:
    """
    List all vehicles.

    Args:
    ----
    session: An SQLAlchemy Session object.
    offset: The offset of the data.
    limit: The limit of the displayed data.

    Returns:
    -------
    A list of `schemas.Vehicle` objects representing the vehicles.

    """
    vehicles = repository.factory(models.Vehicle).get_all(
        session=session,
        offset=offset,
        limit=limit,
    )
    return [schemas.Vehicle.from_orm(vehicle) for vehicle in vehicles]


def filter_by(
    session: Session,
    filter_by: FilterBy,
    value: str,
) -> list[schemas.Vehicle]:
    """
    Filter vehicles based on a specified criterion.

    Args:
    ----
    session: An SQLAlchemy Session object.
    filter_by: The criterion to filter the vehicles by.
    Should be one of the values in `FilterBy` enum.
    value: The value to filter the vehicles by.
    Should be a string, integer, or boolean depending on the criterion.

    Returns:
    -------
    A list of `schemas.Vehicle` objects representing the filtered vehicles.

    Raises:
    ------
    HTTPError: If the value provided is of an invalid type for the specified criterion.

    """
    match filter_by:
        case FilterBy.NAME:
            vehicles = repository.factory(models.Vehicle).filter_by(
                session=session,
                filter_by={"name": value},
            )
        case FilterBy.YEAR_OF_MANUFACTURE:
            try:
                parsed = int(value)
            except ValueError as e:
                raise HTTPError(
                    status_code=422,
                    detail=f"{UNPROCESSABLE} integer.",
                ) from e
            else:
                vehicles = repository.factory(models.Vehicle).filter_by(
                    session=session,
                    filter_by={"year_of_manufacture": parsed},
                )
        case FilterBy.READY_TO_DRIVE:
            parsed = _str2bool(value)
            vehicles = repository.factory(models.Vehicle).filter_by(
                session=session,
                filter_by={"ready_to_drive": parsed},
            )
    return [schemas.Vehicle.from_orm(vehicle) for vehicle in vehicles]


def _str2bool(value: str) -> bool:
    """Convert a string to a boolean."""
    return value.lower() in {"yes", "true", "t", "1"}


def update(
    session: Session,
    id: int,  # noqa: A002
    update_with: schemas.VehicleUpdate,
) -> schemas.Vehicle:
    """
    Update a vehicle with new information.

    Args:
    ----
    session: An SQLAlchemy Session object.
    id: The ID of the vehicle to update.
    update_with: The updated information for the vehicle,
    provided as a `schemas.VehicleUpdate` object.

    Returns:
    -------
    A `schemas.Vehicle` object representing the updated vehicle.

    Raises:
    ------
    HTTPError: If the vehicle with the specified ID is not found.

    """
    if not (
        to_update := repository.factory(models.Vehicle).get(
            session=session,
            id=id,
        )
    ):
        raise HTTPError(status_code=404, detail="Vehicle not found.")

    to_update = repository.factory(models.Vehicle).update(
        session=session,
        to_update=to_update,
        update_with=update_with,
    )
    return schemas.Vehicle.from_orm(to_update)


def delete(session: Session, id: int) -> None:  # noqa: A002
    """
    Delete a vehicle by ID.

    Arguments:
    ---------
    session: An SQLAlchemy Session object.
    id: The ID of the vehicle to delete.

    Returns:
    -------
    None

    Raises:
    ------
    HTTPError: If the vehicle with the specified ID is not found.

    """
    if repository.factory(models.Vehicle).remove(session=session, id=id):
        return
    raise HTTPError(status_code=404, detail="Vehicle not found.")
