from src.agents import tool_metadata, Parameter
from src.agents.adapters import create_all_tools_str, to_object, extract_tool, extract_args

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

"""

def test_create_all_tools_str():
    assert create_all_tools_str([mock_tool_a, mock_tool_b]) == expected_tools_str


expected_tools_object = """{"description": "A test tool", "name": "Mock Tool A", "parameters": {"input": {"type": "string", "description": "A string"}, "optional": {"type": "string", "description": "A string"}}}"""

def test_to_object():
    assert to_object(mock_tool_a) == expected_tools_object


# def test_extract_tool_success():
#     assert convert_to_mistral_tool(mock_tool) == expected_output


# def test_extract_tool_failure():
#     assert convert_to_mistral_tool(mock_tool) == expected_output


# def test_extract_args_failure():
#     assert convert_to_mistral_tool(mock_tool) == expected_output


# def test_extract_args_failure():
#     assert convert_to_mistral_tool(mock_tool) == expected_output
