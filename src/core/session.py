"""Sqlalchemy related module."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings


def fetch_db_uri() -> str:
    """
    Fetch the database URI from the settings.

    Returns
    -------
    The database URI as a string.

    Raises
    ------
    ValueError: If the SQLALCHEMY_DATABASE_URI is not set in the .env file.

    """
    if not settings.SQLALCHEMY_DATABASE_URI:
        msg = "SQLALCHEMY_DATABASE_URI is not set in .env file."
        raise ValueError(msg)
    return settings.SQLALCHEMY_DATABASE_URI


engine = create_engine(fetch_db_uri(), pool_pre_ping=True, echo=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
