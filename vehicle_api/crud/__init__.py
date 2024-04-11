"""crud Module."""

from vehicle_api.crud.crud import AbstractRepository
from vehicle_api.crud.sqlalchemy_repo import SQLAlchemyRepository

__all__ = ["AbstractRepository", "SQLAlchemyRepository"]
