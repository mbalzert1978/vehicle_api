from unittest.mock import MagicMock

import pytest
from fastapi import Request
from loguru import logger

from app.middlewares.log import create_log_message, get_log_strategy


def get_request_object(
    client: str = "TestClient",
    method: str = "GET",
    url: str = "/api/v1/vehicles",
) -> MagicMock:
    request = MagicMock(spec=Request)
    request.client = client
    request.method = method
    request.url.path = url
    return request


def test_create_log_message_when_given_valid_request_should_return_formatted_log_string() -> (
    None
):
    """
    Given: A Request object with client, method, and url path
    When: create_log_message is called with the Request object
    Then: The log message should include the client, method, and url path
    """
    assert (
        create_log_message(get_request_object())
        == "[TestClient]::[GET]::[/api/v1/vehicles]"
    )


def test_create_log_message_when_given_non_request_object_should_return_empty_string() -> (
    None
):
    """
    Given: A non-Request object
    When: create_log_message is called with the non-Request object
    Then: The log message should be an empty string
    """
    assert create_log_message(None) == ""


@pytest.mark.parametrize(
    "code, logger_fn, expected_message",
    [
        (100, logger.info, "INFORMATIONAL"),
        (200, logger.info, "SUCCESS"),
        (300, logger.info, "REDIRECTION"),
        (400, logger.error, "CLIENT_ERROR"),
        (500, logger.critical, "SERVER_ERROR"),
        (600, logger.warning, "UNKNOWN STATUS CODE: 600"),
    ],
    ids=[
        "test_get_log_strategy_when_given_informational_code_should_return_info_logger_and_informational_message",
        "test_get_log_strategy_when_given_success_code_should_return_info_logger_and_success_message",
        "test_get_log_strategy_when_given_redirection_code_should_return_info_logger_and_redirection_message",
        "test_get_log_strategy_when_given_client_error_code_should_return_error_logger_and_client_error_message",
        "test_get_log_strategy_when_given_server_error_code_should_return_critical_logger_and_server_error_message",
        "test_get_log_strategy_when_given_unknown_code_should_return_warning_logger_and_unknown_status_message",
    ],
)
def test_get_log_strategy_when_given_status_code_should_return_correct_logger_and_message(
    code, logger_fn, expected_message
):
    """
    Given: A status code
    When: get_log_strategy is called with the status code
    Then: It should return the expected logger function and status message
    """
    log_function, status_message = get_log_strategy(code)

    assert log_function == logger_fn
    assert status_message == expected_message
