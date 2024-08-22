from pytest import raises
import pytest
from src.llm.factory import get_llm
from tests.agents import MockAgent, mock_agent_description, mock_agent_name, mock_tools


def test_agent_metadata_description():
    assert MockAgent.description == mock_agent_description


def test_agent_metadata_name():
    assert MockAgent.name == mock_agent_name


def test_agent_metadata_tools():
    assert MockAgent.tools == mock_tools


mock_model = "mockmodel"
mock_llm = get_llm("mockllm")
mock_agent_instance = MockAgent("mockllm", mock_model)


@pytest.mark.asyncio
async def test_agent_invoke_uses_tool(mocker):
    mock_response = """{"tool_name": "Mock Tool A", "tool_parameters": { "input": "value for input" }, "reasoning": "Mock reasoning" }"""  # noqa: E501
    mock_llm.chat = mocker.AsyncMock(return_value=mock_response)

    response = await mock_agent_instance.invoke("Mock task to solve")

    assert response == "value for input"


@pytest.mark.asyncio
async def test_agent_invoke_with_no_tool(mocker):
    mock_response = """{"tool_name": "Undefined Tool", "tool_parameters": {}, "reasoning": "Mock reasoning"}"""
    mock_llm.chat = mocker.AsyncMock(return_value=mock_response)

    with raises(Exception) as error:
        await mock_agent_instance.invoke("Mock task to solve")

    expected = "Unable to extract chosen tool and parameters from {'tool_name': 'Undefined Tool', 'tool_parameters': {}, 'reasoning': 'Mock reasoning'}"  # noqa: E501
    assert str(error.value) == expected


@pytest.mark.asyncio
async def test_agent_invoke_no_appropriate_tool_for_task(mocker):
    mock_response = (
        """{"tool_name": "None", "tool_parameters": {}, "reasoning": "No tool was appropriate for the task"}"""
    )
    mock_llm.chat = mocker.AsyncMock(return_value=mock_response)

    with raises(Exception) as error:
        await mock_agent_instance.invoke("Mock task to solve")

    expected = "Unable to extract chosen tool and parameters from {'tool_name': 'None', 'tool_parameters': {}, 'reasoning': 'No tool was appropriate for the task'}"  # noqa: E501
    assert str(error.value) == expected  # noqa: E501
