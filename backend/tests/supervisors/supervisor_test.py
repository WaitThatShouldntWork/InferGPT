from tests.agents import MockAgent
from src.supervisors import solve_all, solve_task, no_tasks_response, unsolvable_response, no_agent_response

mock_answer = "answer"
scratchpad = []
task = {"query": "Solve this problem"}
intent_json = {
    "query": "example query?",
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
agent = MockAgent()


def test_solve_all_no_tasks():
    answer = solve_all({"questions": []})

    assert answer == no_tasks_response


def test_solve_all_gets_final_answer(mocker):
    task_1_answer = "the answer is 42"
    mocker.patch("src.supervisors.supervisor.solve_task", return_value=("the_best_agent", task_1_answer))

    scratchpad = solve_all(intent_json)
    print(f"Scratchpad: {scratchpad}")
    assert scratchpad[0]["result"] == task_1_answer


def test_solve_task_first_attempt_solves(mocker):
    agent.invoke = mocker.MagicMock(return_value=mock_answer)
    mocker.patch("src.supervisors.supervisor.get_agent_for_task", return_value=agent)
    mocker.patch("src.supervisors.supervisor.is_valid_answer", return_value=True)

    answer = solve_task(task, scratchpad)

    assert answer == (agent.name, mock_answer)


def test_solve_task_unsolvable(mocker):
    agent.invoke = mocker.MagicMock(return_value=mock_answer)
    mocker.patch("src.supervisors.supervisor.get_agent_for_task", return_value=agent)
    mocker.patch("src.supervisors.supervisor.is_valid_answer", return_value=False)

    answer = solve_task(task, scratchpad)

    assert answer == (None, unsolvable_response)


def test_solve_task_no_agent_found(mocker):
    mocker.patch("src.supervisors.supervisor.get_agent_for_task", return_value=None)

    answer = solve_task(task, scratchpad)

    assert answer == (None, no_agent_response)
