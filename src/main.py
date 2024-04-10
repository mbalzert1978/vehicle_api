"""Vehicle api main module."""

import logging

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import OperationalError
from starlette.middleware.cors import CORSMiddleware

from src.api.errors import (
    db_handler,
    http422_error_handler,
    http_error_handler,
    not_found_handler,
    uncought_handler,
)
from src.api.routes.api import router as api_router
from src.core.config import get_app_settings
from src.core.error import HTTPError

logger = logging.getLogger(__name__)

settings = get_app_settings()
settings.configure_logging()


def get_application() -> FastAPI:
    settings = get_app_settings()

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.add_exception_handler(HTTPError, not_found_handler)
    application.add_exception_handler(Exception, uncought_handler)
    application.add_exception_handler(OperationalError, db_handler)

    application.include_router(api_router, prefix=settings.api_prefix)

    return application


app = get_application()
