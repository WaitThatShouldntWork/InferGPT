import json
import logging
from typing import Tuple

from src.utils import get_scratchpad, update_scratchpad
from src.router import get_agent_for_task
from src.agents import validator_agent

no_tasks_response = "No tasks found to solve"
unsolvable_response = "I am sorry, but I was unable to find an answer to this task"
no_agent_response = "I am sorry, but I was unable to find an agent to solve this task"


def solve_all(intent_json):
    questions = intent_json["questions"]

    if len(questions) == 0:
        return no_tasks_response

    for question in questions:
        (agent_name, answer) = solve_task(question, get_scratchpad())
        update_scratchpad(agent_name, question, answer)

    logging.info("Final scratchpad:")
    logging.info(json.dumps(get_scratchpad(), indent=4))

    return get_scratchpad()


def solve_task(task, scratchpad, attempt=0) -> Tuple[str | None, str]:
    if attempt == 5:
        return (None, unsolvable_response)

    agent = get_agent_for_task(task, scratchpad)
    if agent is None:
        return (None, no_agent_response)

    answer = agent.invoke(task)
    if is_valid_answer(answer, task):
        return (agent.name, answer)

    return solve_task(task, scratchpad, attempt + 1)


def is_valid_answer(answer, task):
    is_valid = (validator_agent.invoke(f"Task: {task}  Answer: {answer}")).lower() == "true"
    return is_valid
