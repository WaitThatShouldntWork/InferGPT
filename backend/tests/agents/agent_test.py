from pytest import raises
from src.agents import tool_metadata, Agent, agent_metadata

agent_description = "A test agent"
agent_name = "Mock Agent"
tools = []


@agent_metadata(description=agent_description, name=agent_name, tools=tools)
class MockAgent(Agent):
    pass


tool_name = "Mock Tool"
tool_description = "A test tool"
tool_response = "Tool response!"


@tool_metadata(name=tool_name, description=tool_description, parameters={})
def mock_tool():
    return tool_response


def test_agent_metadata_description():
    assert MockAgent.description == agent_description


def test_agent_metadata_name():
    assert MockAgent.name == agent_name


def test_agent_metadata_tools():
    assert MockAgent.tools == tools


def test_agent_invoke_uses_tool(mocker):
    mock_agent_instance = MockAgent()
    mock_agent_instance.tools = [mock_tool]
    mock_response = """{"tool_name": "Mock Tool", "tool_parameters": {}, "reasoning": "Mock reasoning"}""" # noqa: E501
    mocker.patch("src.agents.agent.call_model", return_value=mock_response)

    response = mock_agent_instance.invoke("Mock Tool")

    assert response == tool_response


def test_agent_invoke_with_no_tool(mocker):
    mock_agent_instance = MockAgent()
    mock_agent_instance.tools = [mock_tool]
    mock_response = """{"tool_name": "Undefined Tool", "tool_parameters": {}, "reasoning": "Mock reasoning"}""" # noqa: E501
    mocker.patch("src.agents.agent.call_model", return_value=mock_response)

    with raises(Exception) as error:
        mock_agent_instance.invoke("Undefined Tool")

    assert str(error.value) == "Unable to extract chosen tool and parameters from {'tool_name': 'Undefined Tool', 'tool_parameters': {}, 'reasoning': 'Mock reasoning'}" # noqa: E501
