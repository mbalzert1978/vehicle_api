"""crud Module."""
from src.crud.crud import AbstractRepository
from src.crud.sqlalchemy_repo import SQLAlchemyRepository

__all__ = ["AbstractRepository", "SQLAlchemyRepository"]
