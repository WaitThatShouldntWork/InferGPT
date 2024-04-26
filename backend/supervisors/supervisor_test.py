from supervisors import solve_all_tasks

hair_task = "I want to save to die my hair blue, again"

# TODO: Mock out LLM call
def test_load_task_step_template():
    try:
        solve_all_tasks(hair_task)
    except Exception:
        raise
