from fastapi import HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from loguru import logger
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from vehicle_api.core.error import HTTPError


async def http_error_handler(request: Request, exc: Exception) -> Response:
    correlation_id = request.headers.get("X-Correlation-ID", "")
    headers = {"Content-Type": "application/problem+json", "X-Correlation-ID": correlation_id}
    client = request.client or None
    err = f"[{client}]::{request.method}::{request.url.path}::"
    match exc:
        case HTTPError():
            logger.error(err + "CLIENT_ERROR")
            return JSONResponse(
                status_code=exc.status_code,
                headers=headers,
                content={
                    "type": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.6.4",
                    "title": "The server did not find a current representation for the target resource.",
                    "detail": exc.detail,
                    "status": exc.status_code,
                },
            )

        case HTTPException():
            logger.error(err + "CLIENT_ERROR")
            return JSONResponse(headers=headers, content={"errors": [exc.detail]}, status_code=exc.status_code)

        case RequestValidationError() | ValidationError():
            logger.error(err + "CLIENT_ERROR")
            return JSONResponse(
                {"errors": exc.errors()},
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            )

        case SQLAlchemyError():
            logger.error(err + "SERVER_ERROR")
            return JSONResponse(
                status_code=503,
                headers=headers,
                content={
                    "type": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.6.4",
                    "title": "Unable to connect to the database.",
                    "detail": exc.code,
                    "status": 503,
                },
            )
        case _:
            logger.error(err + "SERVER_ERROR")
            return JSONResponse(
                status_code=500,
                headers=headers,
                content={
                    "type": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.6.1",
                    "title": "An error occurred while processing the request",
                    "status": 500,
                },
            )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": f"{REF_PREFIX}ValidationError"},
    },
}
