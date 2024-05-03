import json
from src.supervisors import solve_all_tasks

hair_task = """
{
    "tasks": [
        {
            "summary": "Find a hair salon near you",
            "explanation": "To dye your hair we need to find somewhere that offers hair dyes"
        }
    ]
}
"""


# TODO: Mock out LLM call
def test_load_task_step_template(mocker):
    tasks_json = json.loads(hair_task)
    mocker.patch("src.supervisors.supervisor.pick_agent", return_value=str(tasks_json["tasks"][0]))
    try:
        solve_all_tasks(tasks_json)
    except Exception:
        raise
