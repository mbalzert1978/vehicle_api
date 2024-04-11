from sqlalchemy.exc import OperationalError
from starlette.requests import Request
from starlette.responses import JSONResponse


async def db_handler(_: Request, exc: OperationalError) -> JSONResponse:
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
