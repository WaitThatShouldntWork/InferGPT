from typing import Tuple
import logging
from src.utils import get_scratchpad, update_scratchpad
from src.router import get_agent_for_task
from src.agents import get_validator_agent
import json

logger = logging.getLogger(__name__)

no_questions_response = "No questions found to solve"
unsolvable_response = "I am sorry, but I was unable to find an answer to this task"
no_agent_response = "I am sorry, but I was unable to find an agent to solve this task"


async def solve_all(intent_json) -> None:
    questions = intent_json["questions"]

    if len(questions) == 0:
        raise Exception(no_questions_response)

    for question in questions:
        try:
            (agent_name, answer) = await solve_task(question, get_scratchpad())
            update_scratchpad(agent_name, question, answer)
        except Exception as error:
            update_scratchpad(error=error)


async def solve_task(task, scratchpad, attempt=0) -> Tuple[str, str]:
    if attempt == 5:
        raise Exception(unsolvable_response)

    agent = await get_agent_for_task(task, scratchpad)
    if agent is None:
        raise Exception(no_agent_response)
    logger.info(f"Agent selected: {agent.name}")
    logger.info(f"Task: {task}")
    answer = await agent.invoke(task)
    logger.info(f"Answer from the task: {answer}")
    parsed_json = json.loads(answer)
    ignore_validation = parsed_json.get('ignore_validation', '')
    logger.info(f"Ignore Validation: {ignore_validation}")
    # Parse the output
    # parsed_output = parse_output(answer)

    # # Accessing the parsed content and check_validation
    # extracted_content = parsed_output['content'] # type: ignore
    # validation_status = parsed_output['check_validation'] # type: ignore
    # logger.info(f"Validation status: {validation_status}")
    # if(ignore_validation == 'true'):
    #     return (agent.name, answer)
    if(ignore_validation == 'true') or await is_valid_answer(answer, task):
        return (agent.name, answer)
    return await solve_task(task, scratchpad, attempt + 1)


async def is_valid_answer(answer, task) -> bool:
    is_valid = (await get_validator_agent().invoke(f"Task: {task}  Answer: {answer}")).lower() == "true"
    return is_valid
