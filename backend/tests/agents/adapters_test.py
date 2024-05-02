from src.agents import tool_metadata, convert_to_mistral_tool, Parameter

name = "Mock Tool"
description = "A test tool"
param_description = "A string"


@tool_metadata(
    name=name,
    description=description,
    parameters={
        "input": Parameter(type="string", description=param_description, required=True),
        "optional": Parameter(type="string", description=param_description, required=False),
    },
)
def mock_tool(input: str):
    return input


def test_tool_conversion():
    expected_output = {
        "type": "function",
        "function": {
            "description": description,
            "name": "mock_tool",
            "parameters": {
                "type": "object",
                "properties": {
                    "input": {"type": "string", "description": param_description},
                    "optional": {"type": "string", "description": param_description},
                },
                "required": ["input"],
            },
        },
    }

    assert convert_to_mistral_tool(mock_tool) == expected_output
