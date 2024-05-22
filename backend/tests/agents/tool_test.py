from src.agents import Parameter, tool

name = "Mock Tool"
description = "A test tool"


@tool(
    description=description,
    name=name,
    parameters={
        "input": Parameter(description="A string", required=True, type="string"),
        "optional": Parameter(description="A string", required=False, type="string"),
    },
)
def mock_tool():
    return "Hello, World!"


def test_tool_name():
    assert mock_tool.name == name


def test_tool_description():
    assert mock_tool.description == description


def test_tool_input_type():
    assert mock_tool.parameters["input"].type == "string"


def test_tool_input_description():
    assert mock_tool.parameters["input"].description == "A string"


def test_tool_input_required():
    assert mock_tool.parameters["input"].required is True


def test_tool_optional_type():
    assert mock_tool.parameters["optional"].type == "string"


def test_tool_optional_description():
    assert mock_tool.parameters["optional"].description == "A string"


def test_tool_optional_required():
    assert mock_tool.parameters["optional"].required is False


def test_tool_action():
    assert mock_tool.action() == "Hello, World!"


expected_tools_object = """{"description": "A test tool", "name": "Mock Tool", "parameters": {"input": {"type": "string", "description": "A string"}, "optional": {"type": "string", "description": "A string"}}}""" # noqa: E501


def test_to_object():
    assert mock_tool.to_str() == expected_tools_object
