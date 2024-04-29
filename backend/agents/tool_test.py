from agents.tool import tool_metadata
from agents.types import Parameter


name = "Mock Tool"
description = "A test tool"

@tool_metadata(
        description=description,
        name=name,
        parameters={
            "input": Parameter(
                description="A string",
                required=True,
                type="string"
            ),
            "optional": Parameter(
                description="A string",
                required=False,
                type="string"
            )
        }
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
    assert mock_tool.parameters["input"].required == True

def test_tool_optional_type():
    assert mock_tool.parameters["optional"].type == "string"

def test_tool_optional_description():
    assert mock_tool.parameters["optional"].description == "A string"

def test_tool_optional_required():
    assert mock_tool.parameters["optional"].required == False

def test_tool_action():
    assert mock_tool.action == mock_tool
