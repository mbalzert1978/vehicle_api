# ruff: noqa: A003, A002
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, TypeVar

from pydantic import BaseModel

from src.crud.sqlalchemy_repo import SQLAlchemyFetcher
from src.model.vehicle import Base

if TYPE_CHECKING:
    from collections.abc import Sequence

    from src.core.session import AbstractSession
    from src.monads.result import Result

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

REPOSITORY_LOCAL: AbstractRepositoryMaker = SQLAlchemyFetcher


class AbstractRepositoryMaker(Protocol[ModelType]):
    model: ModelType | None = None

    def __call__(self, model_type: ModelType | None = None) -> AbstractRepository | type[AbstractRepository]:
        """Fetch an repository object."""


class AbstractRepository(Protocol[ModelType, CreateSchemaType, UpdateSchemaType]):
    model: ModelType
    """The abstract repository protocol."""

    @staticmethod
    def execute(session: AbstractSession, *, stmnt: str) -> Any:
        """
        Execute a statement in the database.

        Parameters
        ----------
        session : Session
            the database session object.
        stmnt : str
            the statement to execute.
        """

    def get(self, session: AbstractSession, *, id: int) -> Result[ModelType, Exception]:
        """
        Get a ModelType object from the database.

        Parameters
        ----------
        session : Session
            the database session object.
        id : int
            the id of the ModelType object.
        default : T | None, optional
            the default value to return if the ModelType object is not found.
            The default value is None.

        Returns
        -------
        ModelType | T
            the ModelType object or the default value.
        """

    def list(
        self, session: AbstractSession, *, filter_by: dict | None = None,
    ) -> Result[Sequence[ModelType], Exception]:
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

    def create(self, session: AbstractSession, *, to_create: CreateSchemaType) -> Result[ModelType, Exception]:
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

    def update(
        self, session: AbstractSession, *, to_update: ModelType, data: UpdateSchemaType,
    ) -> Result[ModelType, Exception]:
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

    def delete(self, session: AbstractSession, *, id: int) -> Result[ModelType, Exception]:
        """
        Delete a ModelType object from the database.

        Parameters
        ----------
        session : Session
            the database session object.
        id : int
            the id of the ModelType object.
        """
