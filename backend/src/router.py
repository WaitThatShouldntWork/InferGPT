import json
import logging
from src.utils import to_json, Config
from src.utils.user_logger import user_log_info
from src.prompts import PromptEngine
from src.agents import Agent, get_available_agents, get_agent_details
from src.llm import get_llm

logger = logging.getLogger(__name__)
prompt_engine = PromptEngine()
config = Config()

def build_best_next_step_prompt(task, scratchpad):
    agents_details = get_agent_details()
    return prompt_engine.load_prompt(
        "best-next-step",
        task=json.dumps(task, indent=4),
        list_of_agents=json.dumps(agents_details, indent=4),
        history=json.dumps(scratchpad, indent=4),
    )


response_format_prompt = prompt_engine.load_prompt("agent-selection-format")


def build_plan(task, llm, scratchpad, model):
    best_next_step_prompt = build_best_next_step_prompt(task, scratchpad)

    # Call model to choose agent
    logger.info("#####  ~  Calling LLM for next best step  ~  #####")
    user_log_info(f"Scratchpad so far: {scratchpad}", __name__)
    best_next_step = llm.chat(model, response_format_prompt, best_next_step_prompt)

    plan = to_json(best_next_step, "Failed to interpret LLM next step format from step string")
    user_log_info(f"Next best step response: {json.dumps(plan, indent=4)}", __name__)

    return plan


def find_agent_from_name(name):
    agents = get_available_agents()
    return (agent for agent in agents if agent.name == name)


def get_agent_for_task(task, scratchpad) -> Agent | None:
    llm = get_llm(config.router_llm)
    model=config.router_model
    plan = build_plan(task, llm, scratchpad, model)
    agent = next(find_agent_from_name(plan["agent_name"]), None)

    return agent
