import json
import logging
from src.utils import call_model
from src.prompts import PromptEngine

prompt_engine = PromptEngine()


def create_agent_object(agent):
    agent_as_object = {
        "name": agent.name,
        "description": agent.description
    }
    return agent_as_object


def convert_step_to_json(next_step):
    try:
        return json.loads(next_step)
    except Exception:
        raise Exception(f"Failed to interpret LLM next step format from step string\"{next_step}\"")


# TODO: Create pick_agent test with mocked calls
def pick_agent(current_task_object, next_task_object, agents_list, history):
    logging.debug("Picking Agent")

    available_agents_object = [create_agent_object(agent) for agent in agents_list]

    # Generate prompts with tasks
    best_next_step_prompt = prompt_engine.load_prompt(
        "best-next-step",
        current_task=json.dumps(current_task_object, indent=4),
        next_task=json.dumps(next_task_object, indent=4),
        list_of_agents=json.dumps(available_agents_object, indent=4),
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
