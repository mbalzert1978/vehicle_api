"""Vehicle api main module."""

import logging

import asgi_correlation_id as cid
import fastapi
import starlette.middleware.base as sbase
import starlette.middleware.cors as scors
import uuid_utils as uuid

from src import vehicles
from src.config import get_settings
from src.core.logging import configure_logging
from src.middlewares.error_handler import error_handling_middleware
from src.middlewares.log import logging_middleware
from src.middlewares.time import add_process_time_header

logger = logging.getLogger(__name__)


def _is_valid_uuid7(uuid_: str) -> bool:
    """
    Check whether a string is a valid v4 uuid.
    """
    try:
        return bool(uuid.UUID(uuid_, version=7))
    except ValueError:
        return False


def get_application() -> fastapi.FastAPI:
    settings = get_settings()
    configure_logging()

    application = fastapi.FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        scors.CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=settings.CORS_HEADERS,
    )

    application.add_middleware(sbase.BaseHTTPMiddleware, dispatch=add_process_time_header)
    application.add_middleware(sbase.BaseHTTPMiddleware, dispatch=logging_middleware)
    application.add_middleware(sbase.BaseHTTPMiddleware, dispatch=error_handling_middleware)

    application.add_middleware(
        cid.CorrelationIdMiddleware,
        header_name="X-Correlation-ID",
        update_request_header=True,
        generator=lambda: uuid.uuid7().hex,
        validator=_is_valid_uuid7,
        transformer=lambda a: a,
    )

    application.include_router(vehicles.router, tags=vehicles.tags)

    return application


app = get_application()
