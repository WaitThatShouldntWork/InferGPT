from pytest import raises
from agents.agent import Agent, agent_metadata
from agents.tool import tool_metadata

agent_description = "A test agent"
agent_name = "Mock Agent"
prompt = "You are a bot!"
tools = []


@agent_metadata(description=agent_description, name=agent_name, prompt=prompt, tools=tools)
class mock_agent(Agent):
    pass


tool_name = "Mock Tool"
tool_description = "A test tool"
tool_response = "Tool response!"


@tool_metadata(name=tool_name, description=tool_description, parameters={})
def mock_tool():
    return tool_response


def test_agent_metadata_description():
    assert mock_agent.description == agent_description


def test_agent_metadata_name():
    assert mock_agent.name == agent_name


def test_agent_metadata_prompt():
    assert mock_agent.prompt == prompt


def test_agent_metadata_tools():
    assert mock_agent.tools == tools


def test_agent_invoke_uses_tool(mocker):
    mock_agent_instance = mock_agent()
    mock_agent_instance.tools = [mock_tool]
    mocker.patch("utils.call_model_with_tools", return_value=("mock_tool", {}))

    response = mock_agent_instance.invoke("Hello, World!")

    assert response == tool_response


def test_agent_invoke_with_no_tool(mocker):
    mock_agent_instance = mock_agent()
    mock_agent_instance.tools = [mock_tool]
    non_existant_tool_name = "non_existent_tool"
    mocker.patch("agents.agent.call_model_with_tools", return_value=(non_existant_tool_name, {}))

    with raises(ValueError) as error:
        mock_agent_instance.invoke("Hello, World!")

    assert str(error.value) == f"Tool {non_existant_tool_name} not found in agent {mock_agent_instance.name}"
