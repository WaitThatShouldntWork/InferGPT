import json
import logging
from utils import call_model
from prompts import PromptEngine

prompt_engine = PromptEngine()


def convert_agents_to_json_shaped_string(agent):
    agent_as_object = {
        "name": agent.name,
        "description": agent.description
    }
    return agent_as_object


def convert_step_to_json(next_step):
    try:
        return json.loads(next_step)
    except Exception:
        raise Exception("Failed to interpret LLM next step format")


# TODO: Create pick_agent test with mocked calls
def pick_agent(current_task_string, next_task_string, list_of_agents, history):
    logging.debug("Picking agent")

    list_of_agent_string = [convert_agents_to_json_shaped_string(agent) for agent in list_of_agents]

    # Generate prompts with tasks
    best_next_step_prompt = prompt_engine.load_prompt(
        "best-next-step",
        current_task=json.dumps(current_task_string, indent=4),
        next_task=json.dumps(next_task_string, indent=4),
        list_of_agents=json.dumps(list_of_agent_string, indent=4),
        history=history
    )

    response_format_prompt = prompt_engine.load_prompt("agent-selection-format")

    logging.info("best_next_step_prompt:")
    logging.info(best_next_step_prompt)

    # Call model to choose agent
    logging.info("Calling LLM for next best step...")
    best_next_step = call_model(response_format_prompt, best_next_step_prompt)

    next_step_json = convert_step_to_json(best_next_step)
    logging.info("Next best step response:")
    logging.info(json.dumps(next_step_json, indent=4))

    return next_step_json
