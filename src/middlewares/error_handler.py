import typing

from fastapi import HTTPException, Request, Response

from src.api.errors.http_error import http_error_handler
from src.utils.utils import is_success


async def error_handling_middleware(
    request: Request,
    call_next: typing.Callable[[Request], typing.Awaitable[Response]],
) -> Response:
    try:
        response = await call_next(request)
    except Exception as exc:  # noqa: BLE001
        return await http_error_handler(request, exc)
    else:
        if is_success(response.status_code):
            return response
    return await http_error_handler(request, HTTPException(status_code=response.status_code))
