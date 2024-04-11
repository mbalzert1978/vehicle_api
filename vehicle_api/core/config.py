"""Configuration file for the project."""

import functools

from vehicle_api.core.settings.app import AppSettings
from vehicle_api.core.settings.base import AppEnvTypes, BaseAppSettings
from vehicle_api.core.settings.development import DevAppSettings
from vehicle_api.core.settings.production import ProdAppSettings

environments: dict[AppEnvTypes, type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
}


@functools.lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
