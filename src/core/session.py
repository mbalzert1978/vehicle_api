"""Sqlalchemy related module."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.model.sql_alchemy import mapper_registry, vehicle_table
from src.model.vehicle import Vehicle


def fetch_db_uri() -> str:
    """
    Fetch the database URI from the settings.

    Returns
    -------
    The database URI as a string.

    Raises
    ------
    ValueError: If the DATABASE_URI is not set in the .env file.

    """
    if not settings.DATABASE_URI:
        msg = "DATABASE_URI is not set in .env file."
        raise ValueError(msg)
    return settings.DATABASE_URI


engine = create_engine(
    fetch_db_uri(),
    pool_pre_ping=True,
    echo=settings.ECHO,
)
mapper_registry.map_imperatively(Vehicle, vehicle_table)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
