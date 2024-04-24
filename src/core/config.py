"""Configuration file for the project."""

import functools

from src.core.settings.app import AppSettings
from src.core.settings.base import AppEnvTypes, BaseAppSettings
from src.core.settings.development import DevAppSettings
from src.core.settings.production import ProdAppSettings

environments: dict[AppEnvTypes, type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
}


@functools.lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
