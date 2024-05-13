from pytest import raises
from tests.agents import MockAgent, mock_agent_description, mock_agent_name, mock_prompt, mock_tools
from src.agents import tool_metadata


tool_name = "Mock Tool"
tool_description = "A test tool"
tool_response = "Tool response!"


@tool_metadata(name=tool_name, description=tool_description, parameters={})
def mock_tool():
    return tool_response


def test_agent_metadata_description():
    assert MockAgent.description == mock_agent_description


def test_agent_metadata_name():
    assert MockAgent.name == mock_agent_name


def test_agent_metadata_prompt():
    assert MockAgent.prompt == mock_prompt


def test_agent_metadata_tools():
    assert MockAgent.tools == mock_tools


def test_agent_invoke_uses_tool(mocker):
    agent = MockAgent()
    agent.tools = [mock_tool]
    mocker.patch("src.agents.agent.call_model_with_tools", return_value=("mock_tool", {}))

    response = agent.invoke("Hello, World!")

    assert response == tool_response


def test_agent_invoke_with_no_tool(mocker):
    agent = MockAgent()
    agent.tools = [mock_tool]
    non_existant_tool_name = "non_existent_tool"
    mocker.patch("src.agents.agent.call_model_with_tools", return_value=(non_existant_tool_name, {}))

    with raises(ValueError) as error:
        agent.invoke("Hello, World!")

    assert str(error.value) == f"Tool {non_existant_tool_name} not found in agent {agent.name}"
