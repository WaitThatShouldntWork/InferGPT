import json

import pytest
from src.llm import MockLLM
from src.agents import agent_details
from tests.agents import MockAgent, mock_agent_name
from src.router import get_agent_for_task


mock_model = "mockmodel"
mock_llm = MockLLM()
mock_agent = MockAgent("mockllm", mock_model)
mock_agents = [mock_agent]
task = {"summary": "task1"}
scratchpad = []


@pytest.mark.asyncio
async def test_get_agent_for_task_no_agent_found(mocker):
    plan = '{ "agent_name": "this_agent_does_not_exist" }'
    mocker.patch("src.router.get_llm", return_value=mock_llm)
    mocker.patch("src.router.get_available_agents", return_value=mock_agents)
    mocker.patch("src.router.get_agent_details", return_value=[agent_details(mock_agent)])
    mock_llm.chat = mocker.AsyncMock(return_value=plan)

    agent = await get_agent_for_task(task, scratchpad)

    assert agent is None


@pytest.mark.asyncio
async def test_get_agent_for_task_agent_found(mocker):
    plan = {"agent_name": mock_agent_name}
    mocker.patch("src.router.get_llm", return_value=mock_llm)
    mocker.patch("src.router.get_available_agents", return_value=mock_agents)
    mocker.patch("src.router.get_agent_details", return_value=[agent_details(mock_agent)])
    mock_llm.chat = mocker.AsyncMock(return_value=json.dumps(plan))

    agent = await get_agent_for_task(task, scratchpad)

    assert agent is mock_agent
