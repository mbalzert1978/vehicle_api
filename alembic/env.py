from logging.config import fileConfig  # noqa: INP001

from sqlalchemy import engine_from_config, pool

from alembic import context
from src.core.config import settings
from src.domain.models import Base

config = context.config
fileConfig(config.config_file_name)  # type: ignore[arg-type]
target_metadata = Base.metadata


def get_url() -> str:
    if not settings.SQLALCHEMY_DATABASE_URI:
        err = "SQLALCHEMY_DATABASE_URI is not set, check .env file."
        raise ValueError(err)
    return settings.SQLALCHEMY_DATABASE_URI


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()  # type: ignore[index]
    connectable = engine_from_config(
        configuration,  # type: ignore[arg-type]
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
