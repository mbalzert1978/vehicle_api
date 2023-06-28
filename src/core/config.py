"""Configuration file for the project."""
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):

    """Project settings."""

    API_VERSION: str = "v1"
    PROJECT_NAME: str
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str
    SQL_ALCHEMY_ECHO: bool = False
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    @classmethod
    def assemble_db_connection(cls, v: str, values: dict) -> str:
        """
        Assemble the database connection URI.

        Args:
        ----
        v: The input value of the SQLALCHEMY_DATABASE_URI field.
        values: A dictionary with the remaining configuration field values.

        Returns:
        -------
        The assembled database connection URI as a string.

        """
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DATABASE') or ''}",
        )

    class Config:

        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore[call-arg]
