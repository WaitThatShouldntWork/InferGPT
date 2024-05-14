from tests.agents import MockAgent
from src.supervisors import solve_all_tasks, solve_task, no_tasks_response, unsolvable_response, no_agent_response

mock_answer = "answer"
scratchpad = []
task = {"summary": "Solve this problem"}
task_dict = {"tasks": [task]}
agent = MockAgent()


def test_solve_all_tasks_no_tasks():
    answer = solve_all_tasks({"tasks": []})

    assert answer == no_tasks_response


def test_solve_all_tasks_gets_final_answer(mocker):
    task_1_answer = "the answer is 42"
    mocker.patch("src.supervisors.supervisor.solve_task", return_value=("the_best_agent", task_1_answer))

    answer = solve_all_tasks(task_dict)

    assert answer == task_1_answer


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
