import time
import typing

from fastapi import Request, Response


async def add_process_time_header(
    request: Request,
    call_next: typing.Callable[[Request], typing.Awaitable[Response]],
) -> Response:
    start_time = time.perf_counter_ns()
    response = await call_next(request)
    end_time = time.perf_counter_ns()
    prcess_time_in_sec = (end_time - start_time) / 1e6
    response.headers["X-Process-Time-Milliseconds"] = str(prcess_time_in_sec)
    return response
