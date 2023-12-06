"""Vehicle api main module."""
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from src.api.v1.endpoints.service_health import service
from src.api.v1.endpoints.vehicle import router
from src.core.config import get_app_settings
from src.core.error import HTTPError

logger = logging.getLogger(__name__)

settings = get_app_settings()
app = FastAPI(**settings.fastapi_kwargs)


@app.exception_handler(OperationalError)
async def db_error(request: Request, exc: OperationalError) -> JSONResponse:
    msg = "Operational Error on db"
    logger.error(msg, exc, request)
    return JSONResponse(
        status_code=503,
        headers={"Content-Type": "application/problem+json"},
        content={
            "type": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.6.4",
            "title": "Unable to connect to the database.",
            "detail": exc.code,
            "status": 503,
        },
    )


@app.exception_handler(HTTPError)
async def not_found_error(request: Request, exc: HTTPError) -> JSONResponse:
    msg = "Not found."
    logger.info(msg, exc, request)
    return JSONResponse(
        status_code=exc.status_code,
        headers={"Content-Type": "application/problem+json"},
        content={
            "type": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.6.4",
            "title": "The server did not find a current representation for the target resource.",
            "detail": exc.detail,
            "status": exc.status_code,
        },
    )


@app.exception_handler(Exception)
async def uncought_error(request: Request, exc: Exception) -> JSONResponse:
    msg = "Uncought Error"
    logger.error(msg, exc, request)
    return JSONResponse(
        status_code=500,
        headers={"Content-Type": "application/problem+json"},
        content={
            "type": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.6.1",
            "title": "An error occurred while processing the request",
            "status": 500,
        },
    )


app.include_router(router)
app.include_router(service)
