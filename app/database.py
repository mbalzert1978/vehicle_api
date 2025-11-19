from collections.abc import Generator, Sequence
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, Final, Protocol

from fastapi import HTTPException
from sqlalchemy import (
    Connection,
    CursorResult,
    Engine,
    Executable,
    Insert,
    MetaData,
    RowMapping,
    Select,
    Update,
    create_engine,
)
from sqlalchemy.exc import SQLAlchemyError

from app.config import Config, ConfigProvider, get_config_provider
from app.constants import DB_NAMING_CONVENTION

DEFAULT_POOL_SIZE: Final[int] = 10
POOL_PRE_PING_ENABLED: Final[bool] = True


class DatabaseConnection(Protocol):
    """Protocol for database connection operations."""

    def execute(self, statement: Executable) -> CursorResult[Any]:
        """Execute a database statement."""
        ...

    def begin(self) -> Connection:
        """Begin a database transaction."""
        ...


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    """Configuration for database connections."""

    database_url: str
    pool_size: int
    pool_pre_ping: bool
    echo: bool
    echo_pool: bool


@dataclass(frozen=True, slots=True)
class DatabaseEngine:
    """Immutable wrapper for SQLAlchemy engine."""

    _engine: Engine
    _metadata: MetaData

    @property
    def engine(self) -> Engine:
        """Get the SQLAlchemy engine instance."""
        assert self._engine is not None, "Engine cannot be None"
        return self._engine

    @property
    def metadata(self) -> MetaData:
        """Get the SQLAlchemy metadata instance."""
        assert self._metadata is not None, "Metadata cannot be None"
        return self._metadata


class DatabaseConfigFactory:
    """Factory for creating database configuration instances."""

    @staticmethod
    def new_from_config(config: Config) -> DatabaseConfig:
        """Create database configuration from application config.

        Args:
            config: Application configuration instance.

        Returns:
            DatabaseConfig instance with settings from app config.
        """
        assert isinstance(config, Config), "Config must be a Config instance"
        assert config.DATABASE_URL is not None, "Database URL cannot be None"

        database_url = str(config.DATABASE_URL)
        assert database_url.strip(), "Database URL cannot be empty"

        result = DatabaseConfig(
            database_url=database_url,
            pool_size=DEFAULT_POOL_SIZE,
            pool_pre_ping=POOL_PRE_PING_ENABLED,
            echo=config.ENVIRONMENT.is_debug,
            echo_pool=config.ENVIRONMENT.is_debug,
        )

        assert isinstance(result, DatabaseConfig), (
            "Result must be a DatabaseConfig instance"
        )
        assert result.database_url == database_url, "Database URL must be preserved"

        return result


class DatabaseEngineFactory:
    """Factory for creating database engine instances."""

    @staticmethod
    def new(database_config: DatabaseConfig) -> DatabaseEngine:
        """Create a new database engine from configuration.

        Args:
            database_config: Database configuration to use.

        Returns:
            DatabaseEngine instance with configured SQLAlchemy engine.
        """
        assert isinstance(database_config, DatabaseConfig), (
            "Database config must be a DatabaseConfig instance"
        )
        assert database_config.database_url.strip(), "Database URL cannot be empty"
        assert database_config.pool_size > 0, "Pool size must be positive"

        engine = create_engine(
            database_config.database_url,
            echo=database_config.echo,
            pool_size=database_config.pool_size,
            pool_pre_ping=database_config.pool_pre_ping,
            echo_pool=database_config.echo_pool,
        )

        metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

        result = DatabaseEngine(_engine=engine, _metadata=metadata)

        assert isinstance(result, DatabaseEngine), (
            "Result must be a DatabaseEngine instance"
        )
        assert result.engine is not None, "Engine must be created"
        assert result.metadata is not None, "Metadata must be created"

        return result

    @staticmethod
    def new_from_config_provider(config_provider: ConfigProvider) -> DatabaseEngine:
        """Create a new database engine from config provider.

        Args:
            config_provider: Configuration provider instance.

        Returns:
            DatabaseEngine instance configured from provider.
        """
        assert isinstance(config_provider, ConfigProvider), (
            "Config provider must be a ConfigProvider instance"
        )

        database_config = DatabaseConfigFactory.new_from_config(config_provider.config)
        result = DatabaseEngineFactory.new(database_config)

        assert isinstance(result, DatabaseEngine), (
            "Result must be a DatabaseEngine instance"
        )

        return result


_database_engine: DatabaseEngine = DatabaseEngineFactory.new_from_config_provider(
    get_config_provider()
)


def get_database_engine() -> DatabaseEngine:
    """Get the global database engine instance.

    Returns:
        The configured DatabaseEngine instance.
    """
    assert _database_engine is not None, "Database engine must be initialized"
    return _database_engine


def get_connection() -> Generator[Connection, None, None]:
    """Get a database connection within a transaction context.

    Yields:
        Database connection within a transaction.

    Raises:
        HTTPException: If database connection or transaction fails.
    """
    database_engine = get_database_engine()
    assert database_engine is not None, "Database engine cannot be None"

    try:
        with database_engine.engine.begin() as conn:
            assert conn is not None, "Connection cannot be None"
            yield conn
    except (SQLAlchemyError, OSError) as exc:
        assert exc is not None, "Exception cannot be None"
        error_message = str(exc)
        assert error_message.strip(), "Error message cannot be empty"
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail=error_message
        ) from exc


def fetch_one(
    conn: Connection, select_query: Select | Insert | Update
) -> RowMapping | None:
    """Fetch a single row from the database.

    Args:
        conn: Database connection to use.
        select_query: SQL query to execute.

    Returns:
        Single row mapping or None if no results.
    """
    assert isinstance(conn, Connection), "Connection must be a Connection instance"
    assert select_query is not None, "Select query cannot be None"

    cursor: CursorResult[Any] = conn.execute(select_query)
    assert cursor is not None, "Cursor cannot be None"

    result = cursor.mappings().one_or_none()
    assert result is None or isinstance(result, RowMapping), (
        "Result must be RowMapping or None"
    )

    return result


def fetch_all(
    conn: Connection, select_query: Select | Insert | Update
) -> Sequence[RowMapping]:
    """Fetch all rows from the database.

    Args:
        conn: Database connection to use.
        select_query: SQL query to execute.

    Returns:
        Sequence of row mappings.
    """
    assert isinstance(conn, Connection), "Connection must be a Connection instance"
    assert select_query is not None, "Select query cannot be None"

    cursor: CursorResult[Any] = conn.execute(select_query)
    assert cursor is not None, "Cursor cannot be None"

    result = cursor.mappings().all()
    assert isinstance(result, Sequence), "Result must be a Sequence"

    return result


def execute(conn: Connection, select_query: Executable) -> CursorResult[Any]:
    """Execute a database statement.

    Args:
        conn: Database connection to use.
        select_query: SQL statement to execute.

    Returns:
        Cursor result from the executed statement.
    """
    assert isinstance(conn, Connection), "Connection must be a Connection instance"
    assert select_query is not None, "Select query cannot be None"

    result = conn.execute(select_query)
    assert result is not None, "Result cannot be None"
    assert isinstance(result, CursorResult), "Result must be a CursorResult instance"

    return result
