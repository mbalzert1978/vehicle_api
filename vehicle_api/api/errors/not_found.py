from starlette.requests import Request
from starlette.responses import JSONResponse

from vehicle_api.core.error import HTTPError


async def not_found_handler(_: Request, exc: HTTPError) -> JSONResponse:
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
