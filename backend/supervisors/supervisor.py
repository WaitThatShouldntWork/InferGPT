import logging
from router import pick_agent

def solve_all_tasks(tasks_json):

    first_task = tasks_json["tasks"][0]
    logging.info("solving first task: " + str(first_task))

    next_step_json = pick_agent(str(first_task))
    logging.info("agent picked: " + next_step_json["agent"])

    return next_step_json["agent"]
