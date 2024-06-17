import json
from tests.llm import MockLLM
from tests.agents import MockAgent, mock_agent_name
from src.router import get_agent_for_task


mock_model = MockLLM()
mock_agent = MockAgent(mock_model)
mock_agents = [mock_agent]
task = {"summary": "task1"}
scratchpad = []


def test_get_agent_for_task_no_agent_found(mocker):
    plan = '{ "agent_name": "this_agent_does_not_exist" }'
    mocker.patch("src.router.agents", mock_agents)
    mock_model.chat = mocker.MagicMock(return_value=plan)

    agent = get_agent_for_task(task, mock_model, scratchpad)

    assert agent is None


def test_get_agent_for_task_agent_found(mocker):
    plan = {"agent_name": mock_agent_name}
    mocker.patch("src.router.agents", mock_agents)
    mock_model.chat = mocker.MagicMock(return_value=json.dumps(plan))

    agent = get_agent_for_task(task, mock_model, scratchpad)

    assert agent is mock_agent
