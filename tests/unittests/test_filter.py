import pytest

from src.core.error import HTTPError
from src.service.services import _parse_bool, _parse_int


# Arrange

# Happy path tests
@pytest.mark.parametrize(
    "value, expected",
    [
        # Test case 1: "yes" (lowercase)
        ("yes", True),
        # Test case 2: "true" (lowercase)
        ("true", True),
        # Test case 3: "t" (lowercase)
        ("t", True),
        # Test case 4: "1"
        ("1", True),
        # Test case 5: "no" (lowercase)
        ("no", False),
        # Test case 6: "false" (lowercase)
        ("false", False),
        # Test case 7: "f" (lowercase)
        ("f", False),
        # Test case 8: "0"
        ("0", False),
    ],
    ids=["yes", "true", "t", "1", "no", "false", "f", "0"],
)
def test_parse_bool_happy_path(value, expected):
    # Act
    result = _parse_bool(value)

    # Assert
    assert result == expected


# Edge cases
@pytest.mark.parametrize(
    "value, expected",
    [
        # Test case 1: Empty string
        ("", False),
        # Test case 2: "YES" (uppercase)
        ("YES", True),
        # Test case 3: "TRUE" (uppercase)
        ("TRUE", True),
        # Test case 4: "T" (uppercase)
        ("T", True),
        # Test case 5: "NO" (uppercase)
        ("NO", False),
        # Test case 6: "FALSE" (uppercase)
        ("FALSE", False),
        # Test case 7: "F" (uppercase)
        ("F", False),
    ],
    ids=["empty_string", "YES", "TRUE", "T", "NO", "FALSE", "F"],
)
def test_parse_bool_edge_cases(value, expected):
    # Act
    result = _parse_bool(value)

    # Assert
    assert result == expected


# Happy path tests
@pytest.mark.parametrize(
    "value, expected",
    [
        # Test case 1: Valid integer string
        ("123", 123),
        # Test case 2: Negative integer string
        ("-456", -456),
        # Test case 3: Zero string
        ("0", 0),
    ],
    ids=["valid_integer_string", "negative_integer_string", "zero_string"],
)
def test_parse_int_happy_path(value, expected):
    # Act
    result = _parse_int(value)

    # Assert
    assert result == expected


# Edge cases
@pytest.mark.parametrize(
    "value, expected",
    [
        # Test case 1: Empty string
        ("", HTTPError(status_code=422, detail="unprocessable value, not a integer.")),
        # Test case 2: Non-integer string
        ("abc", HTTPError(status_code=422, detail="unprocessable value, not a integer.")),
    ],
    ids=["empty_string", "non_integer_string"],
)
def test_parse_int_edge_cases(value, expected):
    # Act & Assert
    with pytest.raises(HTTPError) as exc_info:
        _parse_int(value)
    assert exc_info.value.status_code == expected.status_code
    assert exc_info.value.detail == expected.detail


# Error cases
@pytest.mark.parametrize(
    "value",
    [
        # Test case 1: None value
        (None, HTTPError(status_code=422, detail="unprocessable value, not a integer.")),
        # Test case 2: List value
        (["123"], HTTPError(status_code=422, detail="unprocessable value, not a integer.")),
        # Test case 3: Dictionary value
        ({"value": "123"}, HTTPError(status_code=422, detail="unprocessable value, not a integer."))
    ],
    ids=["none_value", "list_value", "dictionary_value"],
)
def test_parse_int_error_cases(value):
    # Act & Assert
    with pytest.raises(HTTPError):
        _parse_int(value)
