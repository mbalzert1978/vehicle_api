import logging

from pydantic_settings import SettingsConfigDict

from src.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Dev Vehicle API"

    logging_level: int = logging.DEBUG

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
