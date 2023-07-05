"""Services module."""

from sqlalchemy.orm import Session

from src.core.error import HTTPError
from src.crud import repository
from src.domain import schemas, types

UNPROCESSABLE = "unprocessable value, not a"


def fetch_schema(cls_name: str) -> types.BaseModel:
    """Fetch schema from module."""
    return getattr(schemas, cls_name)


def create(
    session: Session,
    data: dict,
    model: type[types.ModelType],
) -> types.BaseModel:
    """
    Create a new object in the database.

    Args:
    ----
    session: An SQLAlchemy Session object.
    data: The data to create the new object.
    model: The model to create.
    """
    schema = fetch_schema(model.__name__)
    create_schema = fetch_schema(f"{model.__name__}Create")
    to_create = create_schema(**data)  # type: ignore[operator]
    obj = repository.factory(model).create(session, to_create=to_create)
    return schema.from_orm(obj)


def get(
    session: Session,
    id: int,  # noqa: A002
    model: type[types.ModelType],
) -> types.BaseModel:
    """
        Get a model by ID.

    Args:
    ----
    session: An SQLAlchemy Session object.
    id: The ID of the model to retrieve.
    model: The model to retrieve.

    Returns:
    -------
    A `model` object representing the retrieved model.

    Raises:
    ------
    HTTPError: If the model with the specified ID is not found.
    """
    schema = fetch_schema(model.__name__)
    if obj := repository.factory(model).get(session, id=id):
        return schema.from_orm(obj)
    raise HTTPError(status_code=404, detail="model not found.")


def list_all(
    session: Session,
    offset: int,
    limit: int,
    model: type[types.ModelType],
) -> list[types.BaseModel]:
    """
    List all models.

    Args:
    ----
    session: An SQLAlchemy Session object.
    offset: The offset of the data.
    limit: The limit of the displayed data.
    model: The model to list.

    Returns:
    -------
    A list of `models` objects representing the models.

    """
    schema = fetch_schema(model.__name__)
    objs = repository.factory(model).get_all(
        session,
        offset=offset,
        limit=limit,
    )
    return [schema.from_orm(obj) for obj in objs]


def filter_by(
    session: Session,
    filter_by: dict,
    model: type[types.ModelType],
) -> list[types.BaseModel]:
    """
    Filter objects based on a specified criterion.

    Args:
    ----
    session: An SQLAlchemy Session object.
    filter_by: The criterion to filter the objects by.
    model: The model to filter.

    Returns:
    -------
    A list of `model` objects representing the filtered objects.

    Raises:
    ------
    HTTPError: If the value provided is of an invalid type for the specified criterion.

    """
    schema = fetch_schema(model.__name__)
    if objs := repository.factory(model).filter_by(session, filter_by):
        return [schema.from_orm(obj) for obj in objs]
    raise HTTPError(status_code=404, detail="model not found.")


def _str2bool(value: str) -> bool:
    """Convert a string to a boolean."""
    return value.lower() in {"yes", "true", "t", "1"}


def update(
    session: Session,
    id: int,  # noqa: A002
    model: type[types.ModelType],
    update_with: type[types.UpdateSchemaType],
) -> types.BaseModel:
    """
    Update a model with new information.

    Args:
    ----
    session: An SQLAlchemy Session object.
    id: The ID of the model to update.
    model: The model to update.
    update_with: The updated information for the model,
    provided as a `schemas.modelUpdate` object.

    Returns:
    -------
    A `model` object representing the updated model.

    Raises:
    ------
    HTTPError: If the model with the specified ID is not found.

    """
    schema = fetch_schema(model.__name__)
    if not (to_update := repository.factory(model).get(session, id=id)):
        raise HTTPError(status_code=404, detail="Vehicle not found.")

    to_update = repository.factory(model).update(
        session,
        to_update=to_update,
        update_with=update_with,
    )
    return schema.from_orm(to_update)


def delete(
    session: Session,
    id: int,  # noqa: A002
    model: type[types.ModelType],
) -> None:
    """
    Delete a model by ID.

    Arguments:
    ---------
    session: An SQLAlchemy Session object.
    id: The ID of the model to delete.
    model: The model to delete.

    Returns:
    -------
    None

    Raises:
    ------
    HTTPError: If the model with the specified ID is not found.

    """
    if repository.factory(model).remove(session, id=id):
        return
    raise HTTPError(status_code=404, detail=f"{model} not found.")
