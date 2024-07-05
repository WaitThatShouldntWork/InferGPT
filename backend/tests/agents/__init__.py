from src.agents import Agent, agent, tool, Parameter

name_a = "Mock Tool A"
name_b = "Mock Tool B"
description = "A test tool"
param_description = "A string"


@tool(
    name=name_a,
    description=description,
    parameters={
        "input": Parameter(type="string", description=param_description, required=True),
        "optional": Parameter(type="string", description=param_description, required=False),
        "another_optional": Parameter(type="string", description=param_description, required=False),
    },
)
def mock_tool_a(input: str, llm, model):
    return input


@tool(
    name=name_b,
    description=description,
    parameters={
        "input": Parameter(type="string", description=param_description, required=True),
        "optional": Parameter(type="string", description=param_description, required=False),
    },
)
def mock_tool_b(input: str, llm, model):
    return input


mock_agent_description = "A test agent"
mock_agent_name = "Mock Agent"
mock_prompt = "You are a bot!"
mock_tools = [mock_tool_a, mock_tool_b]


@agent(name=mock_agent_name, description=mock_agent_description, tools=mock_tools)
class MockAgent(Agent):
    pass


__all__ = ["MockAgent", "mock_agent_description", "mock_agent_name", "mock_tools", "mock_tool_a", "mock_tool_b"]
