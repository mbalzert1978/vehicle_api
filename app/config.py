import functools
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Final

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants import Environment

DEFAULT_SITE_DOMAIN: Final[str] = "vehicle_api.test"
DEFAULT_SITE_NAME: Final[str] = "Vehicle API"
DEFAULT_VERSION: Final[str] = "0.0.1"
DEFAULT_API_PREFIX: Final[str] = "/api/v1"
ENV_FILE_NAME: Final[str] = ".env"
ENV_FILE_ENCODING: Final[str] = "utf-8"
DOCS_URL_PATH: Final[str] = "/docs"
OPENAPI_URL_PATH: Final[str] = "/openapi.json"
REDOC_URL_PATH: Final[str] = "/redoc"


class ExtraTokens(StrEnum):
    """Enumeration for extra token handling in settings."""

    ALLOW = "allow"
    IGNORE = "ignore"
    FORBID = "forbid"


class Config(BaseSettings):
    """Application configuration settings."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_NAME,
        env_file_encoding=ENV_FILE_ENCODING,
        extra=ExtraTokens.ALLOW,
    )

    DATABASE_URL: PostgresDsn

    SITE_DOMAIN: str = DEFAULT_SITE_DOMAIN
    SITE_NAME: str = DEFAULT_SITE_NAME
    VERSION: str = DEFAULT_VERSION

    ENVIRONMENT: Environment = Environment.PRODUCTION

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]
    CORS_METHODS: list[str]

    API_PREFIX: str = DEFAULT_API_PREFIX

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        """Get FastAPI application configuration parameters.

        Returns:
            Dictionary containing FastAPI initialization parameters.
        """
        assert isinstance(self.ENVIRONMENT, Environment), (
            "Environment must be a valid Environment enum"
        )
        assert isinstance(self.SITE_NAME, str), "Site name must be a string"
        assert self.SITE_NAME.strip(), "Site name cannot be empty"
        assert isinstance(self.VERSION, str), "Version must be a string"
        assert self.VERSION.strip(), "Version cannot be empty"
        assert isinstance(self.API_PREFIX, str), "API prefix must be a string"

        openapi_url = OPENAPI_URL_PATH if self.ENVIRONMENT.is_debug else None

        result = {
            "debug": self.ENVIRONMENT.is_debug,
            "docs_url": DOCS_URL_PATH,
            "root_path": self.API_PREFIX,
            "openapi_url": openapi_url,
            "redoc_url": REDOC_URL_PATH,
            "title": self.SITE_NAME,
            "version": self.VERSION,
        }

        assert isinstance(result, dict), "Result must be a dictionary"
        assert "title" in result, "Result must contain title"
        assert "version" in result, "Result must contain version"

        return result


@dataclass(frozen=True, slots=True)
class ConfigProvider:
    """Provider for application configuration."""

    _config: Config

    @property
    def config(self) -> Config:
        """Get the configuration instance.

        Returns:
            The application configuration.
        """
        assert isinstance(self._config, Config), "Config must be a Config instance"
        return self._config


class ConfigFactory:
    """Factory for creating configuration instances."""

    @staticmethod
    def new() -> Config:
        """Create a new configuration instance.

        Returns:
            A new Config instance loaded from environment variables.
        """
        result = Config()  # type: ignore[call-arg]

        assert isinstance(result, Config), "Result must be a Config instance"
        assert hasattr(result, "DATABASE_URL"), "Config must have DATABASE_URL"
        assert hasattr(result, "ENVIRONMENT"), "Config must have ENVIRONMENT"

        return result

    @staticmethod
    def new_provider() -> ConfigProvider:
        """Create a new configuration provider.

        Returns:
            A new ConfigProvider instance with a fresh configuration.
        """
        config = ConfigFactory.new()
        result = ConfigProvider(_config=config)

        assert isinstance(result, ConfigProvider), (
            "Result must be a ConfigProvider instance"
        )

        return result


@functools.lru_cache(maxsize=1)
def get_settings() -> Config:
    """Get cached application settings.

    Returns:
        Cached Config instance.
    """
    result = ConfigFactory.new()

    assert isinstance(result, Config), "Result must be a Config instance"

    return result


@functools.lru_cache(maxsize=1)
def get_config_provider() -> ConfigProvider:
    """Get cached configuration provider.

    Returns:
        Cached ConfigProvider instance.
    """
    result = ConfigFactory.new_provider()

    assert isinstance(result, ConfigProvider), (
        "Result must be a ConfigProvider instance"
    )

    return result
