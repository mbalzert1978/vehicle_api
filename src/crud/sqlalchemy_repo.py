"""Repository for CRUD operations on a model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, text

from src.model.base import Base

from .base import BaseRepository

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.orm import Session


class SQLAlchemyRepository[ModelType: Base](BaseRepository):
    """Repository for CRUD operations on a model with SQLAlchemy ORM."""

    def execute(self, *, stmnt: str) -> None:
        """
        Execute a SQL statement.

        Args:
        ----
        stmnt: The SQL statement to execute.

        """
        with self._sess as session:
            session.execute(text(stmnt))

    def get[U](self, *, id: int, default: U | None = None) -> ModelType | U:
        """
        Retrieve a model instance by its ID.

        Args:
        ----
        id: The ID of the model instance to retrieve.
        default: The value to return if the model instance is not found.

        Returns:
        -------
        The model instance with the specified ID.

        """
        with self._sess as session:
            return session.get(self._model_type, id) or default

    def list(self, *, filter_by: dict | None = None) -> Sequence[ModelType]:
        """
        Retrieve a list of model instances.

        Args:
        ----
        filter_by: A dictionary of key-value pairs to filter by.

        Returns:
        -------
        A list of model instances.

        """
        stmt = select(self._model_type)
        if filter_by:
            stmt = stmt.filter_by(**filter_by)
        with self._sess as session:
            return session.execute(stmt).scalars().all()

    def create[CreateSchemaType: BaseModel](self, *, to_create: CreateSchemaType) -> ModelType:
        """
        Create a new model instance.

        Args:
        ----
        to_create: The data to create the model instance.

        Returns:
        -------
        The created model instance.

        """
        serialized_data = jsonable_encoder(to_create)
        obj = self._model_type(**serialized_data)
        with self._sess as session:
            return self.write_to_database(session, obj)

    @staticmethod
    def write_to_database(session: Session, to_create: ModelType) -> ModelType:
        """
        Write a model instance to the database.

        Args:
        ----
        to_create: The model instance to write to the database.

        Returns:
        -------
        The written model instance.

        """
        session.add(to_create)
        session.commit()
        session.refresh(to_create)
        return to_create

    def update[UpdateSchemaType: BaseModel](self, *, to_update: ModelType, data: UpdateSchemaType) -> ModelType:
        """
        Update a model instance with new data.

        Args:
        ----
        to_update: The model instance to update.
        data: The data to update the model instance with.

        Returns:
        -------
        The updated model instance.

        """
        serialized_data = jsonable_encoder(to_update)
        update_data = self.extract_data(data)
        self.update_fields(to_update, serialized_data, update_data)
        with self._sess as session:
            return self.write_to_database(session, to_update)

    @staticmethod
    def extract_data[UpdateSchemaType: BaseModel](update_with: UpdateSchemaType | dict) -> dict:
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

    def delete(self, *, id: int) -> ModelType | None:
        """
        Remove a model instance by its ID.

        Args:
        ----
        id: The ID of the model instance to remove.

        Returns:
        -------
        The removed model instance if found, or None if not found.

        """
        with self._sess as session:
            if not (obj := session.get(self._model_type, id)):
                return None
            session.delete(obj)
            session.commit()
            return obj
