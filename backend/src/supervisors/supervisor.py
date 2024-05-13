import json
import logging
from typing import Tuple

from src.router import get_agent_for_task
from src.agents import validator_agent

def is_valid_answer(answer, task):
    isValid = (validator_agent.invoke(f"Task: {task}  Answer: {answer}")).lower() == "true"

    logging.info(f"Task: '{task}' Success: '{isValid}'")

    return isValid

def update_scratchpad(scratchpad, agent_name, task, result):
    scratchpad.append({
        "agent_name": agent_name,
        "task": task["summary"],
        "result": result
    })

def solve_task(task, scratchpad, attempt = 0) -> Tuple[str | None, str]:
    if attempt == 5:
        return (None, "I am sorry, but I was unable to find an answer to this task")
    
    agent = get_agent_for_task(task, scratchpad)
    if agent is None:
        return (None, "I am sorry, but I was unable to find an agent to solve this task")

    answer = agent.invoke(task["summary"])
    if is_valid_answer(answer, task):
        return (agent.name, answer)

    update_scratchpad(scratchpad, agent.name, task, answer)
    return solve_task(task, scratchpad, attempt + 1)

def solve_all_tasks(tasks_dict):
    scratchpad = []

    for task in tasks_dict["tasks"]:
        (agent_name, answer) = solve_task(task, scratchpad)
        update_scratchpad(scratchpad, agent_name, task, answer)

    logging.info("Final scratchpad:")
    logging.info(json.dumps(scratchpad, indent=4))

    final_answer = scratchpad[-1]
    return final_answer["result"] # TODO: Add summariser method
