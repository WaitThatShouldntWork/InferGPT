import json
from tests.agents import MockAgent, mock_agent_name
from src.router import get_agent_for_task


mock_agent = MockAgent()
mock_agents = [mock_agent]
task = {"summary": "task1"}
scratchpad = []


def test_get_agent_for_task_no_agent_found(mocker):
    plan = '{ "agent_name": "this_agent_does_not_exist" }'
    mocker.patch("src.router.agents", mock_agents)
    mocker.patch("src.router.call_model", return_value=plan)

    agent = get_agent_for_task(task, scratchpad)

    assert agent is None


def test_get_agent_for_task_agent_found(mocker):
    plan = {"agent_name": mock_agent_name}
    mocker.patch("src.router.agents", mock_agents)
    mocker.patch("src.router.call_model", return_value=json.dumps(plan))

    agent = get_agent_for_task(task, scratchpad)

    assert agent is mock_agent
