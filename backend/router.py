import json
import logging
from utils import call_model
from prompts import PromptEngine

# TODO: Create pick_agent test with mocked calls
prompt_engine = PromptEngine()


def convert_to_json(next_step):
    try:
        return json.loads(next_step)
    except Exception:
        raise Exception("Failed to interpret LLM next step format")

def pick_agent(current_task_string, next_task_string):
    logging.debug("Picking agent")

    list_of_agents = ["database_agent, financial_advisor_agent, web_search_agent"]
    best_next_step_prompt = prompt_engine.load_prompt(
        "best-next-step",
        current_task=current_task_string,
        next_task=next_task_string,
        list_of_agents=list_of_agents
    )
    response_format_prompt = prompt_engine.load_prompt("agent-selection-format")

    best_next_step = call_model(response_format_prompt, best_next_step_prompt)

    next_step_json = convert_to_json(best_next_step)

    logging.info("For iteration:\n" + best_next_step_prompt)
    logging.info("Found next best step:")
    logging.info(next_step_json["thoughts"])

    return next_step_json
