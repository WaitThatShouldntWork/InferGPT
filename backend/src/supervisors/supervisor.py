from typing import Tuple

from src.llm import get_llm
from src.utils import Config, get_scratchpad, update_scratchpad
from src.router import get_agent_for_task
from src.agents import validator_agent

no_questions_response = "No questions found to solve"
unsolvable_response = "I am sorry, but I was unable to find an answer to this task"
no_agent_response = "I am sorry, but I was unable to find an agent to solve this task"

config = Config()
router_llm = get_llm(config.router_llm)


def solve_all(intent_json) -> None:
    questions = intent_json["questions"]

    if len(questions) == 0:
        raise Exception(no_questions_response)

    for question in questions:
        try:
            (agent_name, answer) = solve_task(question, get_scratchpad())
            update_scratchpad(agent_name, question, answer)
        except Exception as error:
            update_scratchpad(error=error)


def solve_task(task, scratchpad, attempt=0) -> Tuple[str, str]:
    if attempt == 5:
        raise Exception(unsolvable_response)

    agent = get_agent_for_task(task, router_llm, scratchpad)
    if agent is None:
        raise Exception(no_agent_response)

    answer = agent.invoke(task)
    if is_valid_answer(answer, task):
        return (agent.name, answer)

    return solve_task(task, scratchpad, attempt + 1)


def is_valid_answer(answer, task) -> bool:
    is_valid = (validator_agent.invoke(f"Task: {task}  Answer: {answer}")).lower() == "true"
    return is_valid
