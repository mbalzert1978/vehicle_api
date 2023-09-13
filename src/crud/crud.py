# ruff: noqa: A003, A002
from collections.abc import Sequence
from typing import Protocol, TypeVar

from pydantic import BaseModel

from src.core.session import Session
from src.model.valueobject import ValueObject
from src.model.vehicle import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
T = TypeVar("T")


class AbstractRepository(Protocol[ModelType, CreateSchemaType,
                                  UpdateSchemaType]):
    """The abstract repository protocol."""

    def execute(self, session: Session, *, stmnt: str) -> None:
        """
        Execute a statement in the database.

        Parameters
        ----------
        session : Session
            the database session object.
        stmnt : str
            the statement to execute.
        """

    def create(self, session: Session, *,
               to_create: CreateSchemaType) -> ModelType:
        """
        Create a ModelType object in the database.

        Parameters
        ----------
        session : Session
            the database session object.
        to_create : CreateSchemaType
            the CreateSchemaType object to create.

        Returns
        -------
        ModelType
            the ModelType object.
        """

    def get(self,
            session: Session,
            *,
            id: ValueObject,
            default: T | None = None) -> ModelType | T:
        """
        Get a ModelType object from the database.

        Parameters
        ----------
        session : Session
            the database session object.
        id : ValueObject
            the id of the ModelType object.
        default : T | None, optional
            the default value to return if the ModelType object is not found.
            The default value is None.

        Returns
        -------
        ModelType | T
            the ModelType object or the default value.
        """

    def list(self,
             session: Session,
             *,
             filter_by: dict | None = None) -> Sequence[ModelType]:
        """
        Get a list of ModelType objects from the database.

        Parameters
        ----------
        session : Session
            the database session object.
        filter_by : dict | None, optional
            the filter by dictionary. The default value is None.

        Returns
        -------
        Sequence[ModelType]
            the list of ModelType objects.
        """

    def update(self, session: Session, *, to_update: ModelType,
               data: UpdateSchemaType) -> ModelType:
        """
        Update a ModelType object in the database.

        Parameters
        ----------
        session : Session
            the database session object.
        to_update : ModelType
            the ModelType object to update.
        data : UpdateSchemaType
            the data to update the ModelType object.

        Returns
        -------
        ModelType
            the updated ModelType object.
        """

    def delete(self, session: Session, *, id: ValueObject) -> ModelType | None:
        """
        Delete a ModelType object from the database.

        Parameters
        ----------
        session : Session
            the database session object.
        id : ValueObject
            the id of the ModelType object.
        """
