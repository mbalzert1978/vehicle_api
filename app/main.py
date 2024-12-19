"""Vehicle api main module."""

import logging

import fastapi
import uuid_utils as uuid
from asgi_correlation_id import CorrelationIdMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app import vehicles
from app.config import get_settings
from app.logging import configure_logging
from app.middlewares.log import logging_middleware
from app.middlewares.time import add_process_time_header
from app.utils.utils import is_valid_uuid7

CORRELATION_HEADER = "X-Correlation-ID"


def get_application() -> fastapi.FastAPI:
    settings = get_settings()
    configure_logging()

    application = fastapi.FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=settings.CORS_HEADERS,
    )

    application.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
    application.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
    application.add_middleware(
        CorrelationIdMiddleware,
        header_name=CORRELATION_HEADER,
        update_request_header=True,
        generator=lambda: uuid.uuid7().hex,
        validator=is_valid_uuid7,
        transformer=lambda a: a,
    )

    application.include_router(vehicles.router)

    return application


app = get_application()
