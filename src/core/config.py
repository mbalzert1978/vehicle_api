"""Configuration file for the project."""
from pydantic import ConfigDict, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    """Project settings."""

    API_VERSION: str = "v1"
    PROJECT_NAME: str
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str
    POSTGRES_PORT: int | None = None
    ECHO: bool = False
    DATABASE_URI: PostgresDsn | None = None

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str, info: ValidationInfo) -> str:
        """
        Assemble the database connection URI.

        Args:
        ----
        v: The input value of the DATABASE_URI field.
        values: A dictionary with the remaining configuration field values.

        Returns:
        -------
        The assembled database connection URI as a string.

        """
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            port=info.data.get("POSTGRES_PORT") or 5432,
            path=f"/{info.data.get('POSTGRES_DATABASE') or 'test'}",
        )


settings = Settings()  # type: ignore[call-arg]
