import pytest
from tests.agents import MockAgent
import json
from src.supervisors import solve_all, solve_task, no_questions_response, unsolvable_response, no_agent_response

mock_model = "mockmodel"
mock_answer = "answer"
scratchpad = []
task = {"query": "Solve this problem"}
query = "example query"
intent_json = {
    "query": query,
    "user_intent": "example intent",
    "questions": [
        {
            "query": "example query",
            "question_intent": "example intent",
            "operation": "example operation",
            "question_category": "example category",
            "parameters": [{"type": "example type", "value": "example value"}],
            "aggregation": "example aggregation",
            "sort_order": "example sort_order",
            "timeframe": "example timeframe",
        }
    ],
}

agent = MockAgent("mockllm", mock_model)


@pytest.mark.asyncio
async def test_solve_all_no_tasks():
    with pytest.raises(Exception) as error:
        await solve_all({"questions": []})
        assert error == no_questions_response


@pytest.mark.asyncio
async def test_solve_all_gets_answer(mocker):
    task_1_answer = "the answer is 42"
    agent_name = "the_best_agent"
    expected_result = [{"agent_name": agent_name, "question": query, "result": task_1_answer, "error": None}]
    mocker.patch("src.supervisors.supervisor.solve_task", return_value=(agent_name, task_1_answer))
    mock_get_scratchpad = mocker.patch("src.utils.get_scratchpad", return_value=expected_result)

    await solve_all(intent_json)

    result = mock_get_scratchpad()
    assert result == expected_result



@pytest.mark.asyncio
async def test_solve_task_first_attempt_solves(mocker):
    # Mock the agent to return a JSON-formatted answer with a 'content' field
    mock_answer = json.dumps({
        "content": "the answer is 42",
        "ignore_validation": "false"
    })
    agent.invoke = mocker.AsyncMock(return_value=mock_answer)
    mocker.patch("src.supervisors.supervisor.get_agent_for_task", return_value=agent)
    mocker.patch("src.supervisors.supervisor.is_valid_answer", return_value=True)
    answer = await solve_task(task, scratchpad)
    mock_answer_json = json.loads(mock_answer)

    # Ensure that the result is returned directly without validation
    assert answer == (agent.name, mock_answer_json.get('content', ''), "success")


@pytest.mark.asyncio
async def test_solve_task_ignore_validation(mocker):
    # Mock the agent to return a JSON-formatted answer with ignore_validation as true
    mock_answer = json.dumps({
        "content": "the answer is 42",
        "ignore_validation": "true"
    })
    agent.invoke = mocker.AsyncMock(return_value=mock_answer)
    mocker.patch("src.supervisors.supervisor.get_agent_for_task", return_value=agent)
    mock_is_valid_answer = mocker.patch("src.supervisors.supervisor.is_valid_answer")

    # Run the solve_task function
    answer = await solve_task(task, scratchpad)
    mock_answer_json = json.loads(mock_answer)

    # Ensure that the result is returned directly without validation
    assert answer == (agent.name, mock_answer_json.get('content', ''), "success")
    mock_is_valid_answer.assert_not_called()  # Validation should not be called

@pytest.mark.asyncio
async def test_solve_task_unsolvable(mocker):
    agent.invoke = mocker.MagicMock(return_value=mock_answer)
    mocker.patch("src.supervisors.supervisor.get_agent_for_task", return_value=agent)
    mocker.patch("src.supervisors.supervisor.is_valid_answer", return_value=False)

    with pytest.raises(Exception) as error:
        await solve_task(task, scratchpad)
        assert error == unsolvable_response


@pytest.mark.asyncio
async def test_solve_task_no_agent_found(mocker):
    mocker.patch("src.supervisors.supervisor.get_agent_for_task", return_value=None)

    with pytest.raises(Exception) as error:
        await solve_task(task, scratchpad)
        assert error == no_agent_response
