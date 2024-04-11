from pydantic_settings import SettingsConfigDict

from vehicle_api.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    model_config = SettingsConfigDict(env_file="prod.env", env_file_encoding="utf-8")
