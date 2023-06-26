from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings


def fetch_db_uri() -> str:
    if not settings.SQLALCHEMY_DATABASE_URI:
        msg = "SQLALCHEMY_DATABASE_URI is not set in .env file."
        raise ValueError(msg)
    return settings.SQLALCHEMY_DATABASE_URI


engine = create_engine(fetch_db_uri(), pool_pre_ping=True, echo=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
