import logging
import typing

from pydantic import PostgresDsn
from pydantic_settings import SettingsConfigDict

from src.core.logging import InterceptHandler
from src.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Vehicle API"
    version: str = "0.0.1"

    database_url: PostgresDsn
    max_connection_count: int = 10
    min_connection_count: int = 10

    api_prefix: str = "/api"

    allowed_hosts: list[str] = ["*"]

    logging_level: int = logging.INFO
    loggers: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    model_config = SettingsConfigDict(validate_assignment=True)

    @property
    def fastapi_kwargs(self) -> dict[str, typing.Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]
