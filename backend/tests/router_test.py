import json
from src.agents import agent_details
from src.llm import get_llm
from tests.agents import MockAgent, mock_agent_name
from src.router import get_agent_for_task


mock_model = get_llm("mockllm")
mock_agent = MockAgent("mockllm")
mock_agents = [mock_agent]
task = {"summary": "task1"}
scratchpad = []


def test_get_agent_for_task_no_agent_found(mocker):
    plan = '{ "agent_name": "this_agent_does_not_exist" }'
    mocker.patch("src.router.get_llm", return_value=mock_model)
    mocker.patch("src.router.get_question_agents", return_value=mock_agents)
    mocker.patch("src.router.get_agent_details", return_value=[agent_details(mock_agent)])
    mock_model.chat = mocker.MagicMock(return_value=plan)

    agent = get_agent_for_task(task, scratchpad)

    assert agent is None


def test_get_agent_for_task_agent_found(mocker):
    plan = {"agent_name": mock_agent_name}
    mocker.patch("src.router.get_llm", return_value=mock_model)
    mocker.patch("src.router.get_question_agents", return_value=mock_agents)
    mocker.patch("src.router.get_agent_details", return_value=[agent_details(mock_agent)])
    mock_model.chat = mocker.MagicMock(return_value=json.dumps(plan))

    agent = get_agent_for_task(task, scratchpad)

    assert agent is mock_agent
