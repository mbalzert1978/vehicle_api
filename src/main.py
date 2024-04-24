"""Vehicle api main module."""

import logging
from uuid import uuid4

from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.middleware import is_valid_uuid4
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.api.routes.api import router as api_router
from src.core.config import get_app_settings
from src.core.logging import configure_logging
from src.middlewares.time import add_process_time_header

from .middlewares.error_handler import error_handling_middleware
from .middlewares.log import logging_middleware

logger = logging.getLogger(__name__)

settings = get_app_settings()
configure_logging()


def get_application() -> FastAPI:
    settings = get_app_settings()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
    application.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
    application.add_middleware(BaseHTTPMiddleware, dispatch=error_handling_middleware)

    application.add_middleware(
        CorrelationIdMiddleware,
        header_name="X-Correlation-ID",
        update_request_header=True,
        generator=lambda: uuid4().hex,
        validator=is_valid_uuid4,
        transformer=lambda a: a,
    )

    application.include_router(api_router, prefix=settings.api_prefix)

    return application


app = get_application()
