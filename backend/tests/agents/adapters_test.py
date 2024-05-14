import pytest
from src.agents import tool_metadata, Parameter
from src.agents.adapters import create_all_tools_str, to_object, extract_tool, validate_args

name_a = "Mock Tool A"
name_b = "Mock Tool B"
description = "A test tool"
param_description = "A string"

@tool_metadata(
    name=name_a,
    description=description,
    parameters={
        "input": Parameter(type="string", description=param_description, required=True),
        "optional": Parameter(type="string", description=param_description, required=False),
    },
)
def mock_tool_a(input: str):
    return input

@tool_metadata(
    name=name_b,
    description=description,
    parameters={
        "input": Parameter(type="string", description=param_description, required=True),
        "optional": Parameter(type="string", description=param_description, required=False),
    },
)
def mock_tool_b(input: str):
    return input

expected_tools_str = """{"description": "A test tool", "name": "Mock Tool A", "parameters": {"input": {"type": "string", "description": "A string"}, "optional": {"type": "string", "description": "A string"}}}

{"description": "A test tool", "name": "Mock Tool B", "parameters": {"input": {"type": "string", "description": "A string"}, "optional": {"type": "string", "description": "A string"}}}

""" # noqa: E501

def test_create_all_tools_str():
    assert create_all_tools_str([mock_tool_a, mock_tool_b]) == expected_tools_str


expected_tools_object = """{"description": "A test tool", "name": "Mock Tool A", "parameters": {"input": {"type": "string", "description": "A string"}, "optional": {"type": "string", "description": "A string"}}}""" # noqa: E501

def test_to_object():
    assert to_object(mock_tool_a) == expected_tools_object


def test_extract_tool_success():
    assert extract_tool("Mock Tool A", [mock_tool_a, mock_tool_b]) == mock_tool_a


def test_extract_tool_failure():
    with pytest.raises(Exception, match="Unable to find tool Mock Tool Z in available tools"):
        extract_tool("Mock Tool Z", [mock_tool_a, mock_tool_b])


def test_extract_tool_no_tool_found():
    with pytest.raises(Exception, match="No tool deemed appropriate for task"):
        extract_tool("None", [mock_tool_a, mock_tool_b])


def test_validate_args_success():
    valid_args = {
        "input": "An example string value for input",
        "optional": "An example optional string value for optional"
    }
    try:
        validate_args(valid_args, mock_tool_a)
    except Exception:
        pytest.fail("Error: Valid arguments thrown Exception in validate_args")


# TODO add checks for optional arguments being valid both present and absent in call

def test_validate_args_failure():
    invalid_args = {
        "argument": "An example string value for argument"
    }
    with pytest.raises(Exception, match=r"Unable to fit parameters .* to Tool arguments .*"):
        validate_args(invalid_args, mock_tool_a)
