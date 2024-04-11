import datetime
import http


def utc_now() -> datetime.datetime:
    """Returns the UTC now datetime object."""
    return datetime.datetime.now(tz=datetime.timezone.utc)


def is_success(status_code: int) -> bool:
    return http.HTTPStatus.OK <= status_code < http.HTTPStatus.MULTIPLE_CHOICES


def is_client_error(status_code: int) -> bool:
    return http.HTTPStatus.BAD_REQUEST <= status_code < http.HTTPStatus.INTERNAL_SERVER_ERROR


def is_server_error(status_code: int) -> bool:
    return status_code >= http.HTTPStatus.INTERNAL_SERVER_ERROR
