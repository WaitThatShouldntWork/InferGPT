import json
import logging
from src.utils import to_json, Config
from src.prompts import PromptEngine
from src.agents import Agent, agents, agents_details
from src.llm import get_llm

prompt_engine = PromptEngine()
config = Config()

llm = get_llm(config.router_llm)


def build_best_next_step_prompt(task, scratchpad):
    return prompt_engine.load_prompt(
        "best-next-step",
        task=json.dumps(task, indent=4),
        list_of_agents=json.dumps(agents_details, indent=4),
        history=json.dumps(scratchpad, indent=4),
    )


response_format_prompt = prompt_engine.load_prompt("agent-selection-format")


def build_plan(task, llm, scratchpad):
    best_next_step_prompt = build_best_next_step_prompt(task, scratchpad)

    # Call model to choose agent
    logging.info("#####  ~  Calling LLM for next best step  ~  #####")

    logging.info("Scratchpad so far:")
    logging.info(scratchpad)
    best_next_step = llm.chat(response_format_prompt, best_next_step_prompt)

    plan = to_json(best_next_step, "Failed to interpret LLM next step format from step string")
    logging.info("Next best step response:")
    logging.info(json.dumps(plan, indent=4))

    return plan


def find_agent_from_name(name):
    return (agent for agent in agents if agent.name == name)


def get_agent_for_task(task, scratchpad) -> Agent | None:
    plan = build_plan(task, llm, scratchpad)
    agent = next(find_agent_from_name(plan["agent_name"]), None)

    return agent
