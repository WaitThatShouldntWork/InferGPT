import json
import logging
from src.utils import call_model
from src.prompts import PromptEngine
from src.agents import Agent, agents, agents_details

prompt_engine = PromptEngine()

def convert_step_to_json(next_step):
    try:
        return json.loads(next_step)
    except Exception:
        raise Exception(f"Failed to interpret LLM next step format from step string\"{next_step}\"")

def build_best_next_step_prompt(task, scratchpad):
    return prompt_engine.load_prompt(
        "best-next-step",
        task=json.dumps(task, indent=4),
        list_of_agents=json.dumps(agents_details, indent=4),
        history=json.dumps(scratchpad, indent=4)
    )

response_format_prompt = prompt_engine.load_prompt("agent-selection-format")

# TODO: Create get_plan test with mocked calls
def get_plan(task, scratchpad):
    best_next_step_prompt = build_best_next_step_prompt(task, scratchpad)

    logging.info("best_next_step_prompt:")
    logging.info(best_next_step_prompt)

    # Call model to choose agent
    logging.info("Calling LLM for next best step...")
    best_next_step = call_model(response_format_prompt, best_next_step_prompt)

    plan = convert_step_to_json(best_next_step)
    logging.info("Next best step response:")
    logging.info(json.dumps(plan, indent=4))

    return plan

def find_agent_from_name(name):
    return (agent for agent in agents if agent.name == name)

def get_agent_for_task(task, scratchpad) -> Agent | None:
    plan = get_plan(task, scratchpad)
    agent = next(find_agent_from_name(plan["agent_name"]), None)

    return agent