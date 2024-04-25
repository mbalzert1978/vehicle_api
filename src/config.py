import functools
import typing

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import Environment


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    DATABASE_URL: PostgresDsn

    SITE_DOMAIN: str = "vehicle_api.test"
    SITE_NAME: str = "Vehicle API"
    VERSION: str = "0.0.1"

    ENVIRONMENT: Environment = Environment.PRODUCTION

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]
    CORS_METHODS: list[str]

    API_PREFIX: str = "/api/v1"

    @property
    def fastapi_kwargs(self) -> dict[str, typing.Any]:
        return {
            "debug": self.ENVIRONMENT.is_debug,
            "docs_url": "/docs",
            "root_path": self.API_PREFIX,
            "openapi_url": "/openapi.json" if self.ENVIRONMENT.is_debug else None,
            "redoc_url": "/redoc",
            "title": self.SITE_NAME,
            "version": self.VERSION,
        }


@functools.lru_cache
def get_settings() -> Config:
    return Config()  # type: ignore[call-arg]
