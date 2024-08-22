import pytest
from src.utils import to_json


def test_to_json_success():
    input = '{"key": "value"}'

    assert to_json(input) == {"key": "value"}


def test_to_json_failure():
    input = "invalid"

    with pytest.raises(Exception) as error:
        to_json(input)

    assert str(error.value) == f'Failed to interpret JSON: "{input}"'
