import pytest
from tests.agents import mock_tool_a, mock_tool_b
from src.agents.adapters import create_all_tools_str, extract_tool, validate_args

expected_tools_str = """{"description": "A test tool", "name": "Mock Tool A", "parameters": {"input": {"type": "string", "description": "A string"}, "optional": {"type": "string", "description": "A string"}, "another_optional": {"type": "string", "description": "A string"}}}

{"description": "A test tool", "name": "Mock Tool B", "parameters": {"input": {"type": "string", "description": "A string"}, "optional": {"type": "string", "description": "A string"}}}

"""  # noqa: E501


def test_create_all_tools_str():
    assert create_all_tools_str([mock_tool_a, mock_tool_b]) == expected_tools_str


def test_extract_tool_success():
    assert extract_tool("Mock Tool A", [mock_tool_a, mock_tool_b]) == mock_tool_a


def test_extract_tool_failure():
    with pytest.raises(Exception, match="Unable to find tool Mock Tool Z in available tools"):
        extract_tool("Mock Tool Z", [mock_tool_a, mock_tool_b])


def test_extract_tool_no_tool_found():
    with pytest.raises(Exception, match="No tool deemed appropriate for task"):
        extract_tool("None", [mock_tool_a, mock_tool_b])


def test_validate_all_args_success():
    valid_args = {
        "input": "An example string value for input",
        "optional": "An example optional string value for optional",
        "another_optional": "An example optional string value for another_optional",
    }
    try:
        validate_args(valid_args, mock_tool_a)
    except Exception:
        pytest.fail("Error: Valid arguments thrown Exception in validate_args")


def test_validate_args_some_optional_passed_success():
    valid_args = {
        "input": "An example string value for input",
        "optional": "An example optional string value for optional",
    }
    try:
        validate_args(valid_args, mock_tool_a)
    except Exception:
        pytest.fail("Error: Valid arguments thrown Exception in validate_args")


def test_validate_args_no_optional_passed_success():
    valid_args = {"input": "An example string value for input"}
    try:
        validate_args(valid_args, mock_tool_a)
    except Exception:
        pytest.fail("Error: Valid arguments thrown Exception in validate_args")


def test_validate_args_failure():
    invalid_args = {"argument": "An example string value for argument"}
    with pytest.raises(Exception, match=r"Unable to fit parameters .* to Tool arguments .*: Wrong params"):
        validate_args(invalid_args, mock_tool_a)


def test_validate_extra_args_failure():
    invalid_args = {
        "input": "An example string value for input",
        "optional": "An example optional string value for optional",
        "another_optional": "An example optional string value for another_optional",
        "argument": "An example string value for argument",
    }
    with pytest.raises(Exception, match=r"Unable to fit parameters .* to Tool arguments .*: Extra params"):
        validate_args(invalid_args, mock_tool_a)
