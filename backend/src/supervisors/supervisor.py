import json
import logging
from typing import Tuple

from src.utils import clear_scratchpad, get_scratchpad, update_scratchpad
from src.router import get_agent_for_task
from src.agents import validator_agent


def is_valid_answer(answer, task):
    is_valid = (validator_agent.invoke(f"Task: {task}  Answer: {answer}")).lower() == "true"

    return is_valid


unsolvable_response = "I am sorry, but I was unable to find an answer to this task"
no_agent_response = "I am sorry, but I was unable to find an agent to solve this task"


def solve_task(task, scratchpad, attempt=0) -> Tuple[str | None, str]:
    if attempt == 5:
        return (None, unsolvable_response)

    agent = get_agent_for_task(task, scratchpad)
    if agent is None:
        return (None, no_agent_response)

    answer = agent.invoke(task["summary"])
    if is_valid_answer(answer, task):
        return (agent.name, answer)

    update_scratchpad(agent.name, task, answer)
    return solve_task(task, scratchpad, attempt + 1)


no_tasks_response = "No tasks found to solve"


def solve_all_tasks(tasks_dict):
    tasks = tasks_dict["tasks"]

    if len(tasks) == 0:
        return no_tasks_response

    for task in tasks:
        (agent_name, answer) = solve_task(task, get_scratchpad())
        update_scratchpad(agent_name, task, answer)

    logging.info("Final scratchpad:")
    logging.info(json.dumps(get_scratchpad(), indent=4))

    final_answer = get_scratchpad()[-1]
    clear_scratchpad()
    return final_answer["result"]  # TODO: Add summariser method
