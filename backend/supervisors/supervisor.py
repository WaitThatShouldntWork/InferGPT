import logging
from router import pick_agent


def solve_all_tasks(tasks_json):
    first_task = str(tasks_json["tasks"][0])
    second_task = str(tasks_json["tasks"][1])

    best_next_step_json = pick_agent(first_task, second_task)
    logging.info("agent picked: " + best_next_step_json["agent"])

    return best_next_step_json["thoughts"]["speak"]
