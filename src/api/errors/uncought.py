from starlette.requests import Request
from starlette.responses import JSONResponse


async def uncought_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        headers={"Content-Type": "application/problem+json"},
        content={
            "type": "https://datatracker.ietf.org/doc/html/rfc7231#section-6.6.1",
            "title": "An error occurred while processing the request",
            "status": 500,
        },
    )
