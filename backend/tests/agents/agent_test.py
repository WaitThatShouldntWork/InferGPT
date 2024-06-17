from pytest import raises
from tests.llm import MockLLM
from tests.agents import MockAgent, mock_agent_description, mock_agent_name, mock_tools


def test_agent_metadata_description():
    assert MockAgent.description == mock_agent_description


def test_agent_metadata_name():
    assert MockAgent.name == mock_agent_name


def test_agent_metadata_tools():
    assert MockAgent.tools == mock_tools

mock_model = MockLLM()

def test_agent_invoke_uses_tool(mocker):
    mock_agent_instance = MockAgent(mock_model)

    mock_response = """{"tool_name": "Mock Tool A", "tool_parameters": { "input": "value for input" }, "reasoning": "Mock reasoning" }""" # noqa: E501
    mock_model.chat = mocker.MagicMock(return_value=mock_response)

    response = mock_agent_instance.invoke("Mock task to solve")

    assert response == "value for input"


def test_agent_invoke_with_no_tool(mocker):
    mock_agent_instance = MockAgent(mock_model)
    mock_response = """{"tool_name": "Undefined Tool", "tool_parameters": {}, "reasoning": "Mock reasoning"}"""
    mock_model.chat = mocker.MagicMock(return_value=mock_response)

    with raises(Exception) as error:
        mock_agent_instance.invoke("Mock task to solve")

    assert str(error.value) == "Unable to extract chosen tool and parameters from {'tool_name': 'Undefined Tool', 'tool_parameters': {}, 'reasoning': 'Mock reasoning'}" # noqa: E501


def test_agent_invoke_no_appropriate_tool_for_task(mocker):
    mock_agent_instance = MockAgent(mock_model)
    mock_response = """{"tool_name": "None", "tool_parameters": {}, "reasoning": "No tool was appropriate for the task"}""" # noqa: E501
    mock_model.chat = mocker.MagicMock(return_value=mock_response)

    with raises(Exception) as error:
        mock_agent_instance.invoke("Mock task to solve")

    assert str(error.value) == "Unable to extract chosen tool and parameters from {'tool_name': 'None', 'tool_parameters': {}, 'reasoning': 'No tool was appropriate for the task'}" # noqa: E501
