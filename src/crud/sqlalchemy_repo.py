"""Repository for CRUD operations on a model."""
from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, text

from src.model.vehicle import Base
from src.monads.result import Err, Ok, Result

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class SQLAlchemyFetcher(Generic[ModelType]):
    """Factory for SQLAlchemy repo instances for a database."""

    def __init__(self, model: type[ModelType] | None = None) -> None:
        self.model = model

    def __call__(
        self,
    ) -> SQLAlchemyRepository[ModelType] | type[SQLAlchemyRepository]:
        """
        Return a SQLAlchemyRepository instance.

        Returns
        -------
        A SQLAlchemyRepository instance.

        """
        return SQLAlchemyRepository(self.model) if self.model else SQLAlchemyRepository


class SQLAlchemyRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Repository for CRUD operations on a model with SQLAlchemy ORM."""

    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    @staticmethod
    def execute(session: Session, *, stmnt: str) -> None:
        """
        Execute a SQL statement.

        Args:
        ----
        session: An SQLAlchemy Session object.
        stmnt: The SQL statement to execute.

        """
        session.execute(text(stmnt))

    def get(self, session: Session, *, id: int) -> Result[ModelType, Exception]:
        """
        Retrieve a model instance by its ID.

        Args:
        ----
        session: An SQLAlchemy Session object.
        id: The ID of the model instance to retrieve.
        default: The value to return if the model instance is not found.

        Returns:
        -------
        Result[ModelType, Exception]

        """
        try:
            return Ok(session.get(self.model, id))
        except Exception as exc:
            return Err(exc)

    def list(self, session: Session, *, filter_by: dict | None = None) -> Result[Sequence[ModelType], Exception]:
        """
        Retrieve a list of model instances.

        Args:
        ----
        session: An SQLAlchemy Session object.
        filter_by: A dictionary of key-value pairs to filter by.

        Returns:
        -------
        Result[Sequence[ModelType], Exception]

        """
        try:
            stmt = select(self.model)
            if filter_by:
                stmt = stmt.filter_by(**filter_by)
            return Ok(session.execute(stmt).scalars().all())
        except Exception as exc:
            return Err(exc)

    def create(self, session: Session, *, to_create: CreateSchemaType) -> Result[ModelType, Exception]:
        """
        Create a new model instance.

        Args:
        ----
        session: An SQLAlchemy Session object.
        to_create: The data to create the model instance.

        Returns:
        -------
        Result[ModelType, Exception]

        """
        try:
            serialized_data = jsonable_encoder(to_create)
            obj = self.model(**serialized_data)
            return Ok(self.write_to_database(session, obj))
        except Exception as exc:
            return Err(exc)

    @staticmethod
    def write_to_database(session: Session, to_create: ModelType) -> ModelType:
        """
        Write a model instance to the database.

        Args:
        ----
        session: An SQLAlchemy Session object.
        to_create: The model instance to write to the database.

        Returns:
        -------
        The written model instance.

        """
        session.add(to_create)
        session.commit()
        session.refresh(to_create)
        return to_create

    def update(
        self, session: Session, *, to_update: ModelType, data: UpdateSchemaType,
    ) -> Result[ModelType, Exception]:
        """
        Update a model instance with new data.

        Args:
        ----
        session: An SQLAlchemy Session object.
        to_update: The model instance to update.
        data: The data to update the model instance with.

        Returns:
        -------
        Result[ModelType, Exception]

        """
        try:
            serialized_data = jsonable_encoder(to_update)
            update_data = self.extract_data(data)
            self.update_fields(to_update, serialized_data, update_data)
            return Ok(self.write_to_database(session, to_update))
        except Exception as exc:
            return Err(exc)

    @staticmethod
    def extract_data(update_with: UpdateSchemaType | dict) -> dict:
        """
        Extract the update data from the given object.

        Args:
        ----
        update_with: The object containing the update data.

        Returns:
        -------
        The extracted update data as a dictionary.

        """
        return update_with if isinstance(update_with, dict) else update_with.model_dump(exclude_unset=True)

    @staticmethod
    def update_fields(to_update: ModelType, serialized_data: dict, update_data: dict) -> None:
        """
        Update the fields of a model instance with new data.

        Args:
        ----
        to_update: The model instance to update.
        serialized_data: The serialized data of the model instance.
        update_data: The data containing the fields to update.

        Returns:
        -------
        None

        """
        for field in serialized_data:
            if field not in update_data:
                continue
            setattr(to_update, field, update_data[field])

    def delete(self, session: Session, *, to_delete: ModelType) -> Result[ModelType, Exception]:
        """
        Delete the model instance from the database.

        Args
        ----------
        session: An SQLAlchemy Session object.
        to_delete: The model instance to delete.

        Returns
        -------
        Result[ModelType, Exception]
        """
        try:
            session.delete(to_delete)
            session.commit()
            return Ok(to_delete)
        except Exception as exc:
            return Err(exc)
