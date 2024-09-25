import json
import logging
from src.llm.llm import LLM
from src.utils import to_json, Config
from src.utils.log_publisher import publish_log_info, LogPrefix
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


async def build_plan(task, llm: LLM, scratchpad, model):
    best_next_step_prompt = build_best_next_step_prompt(task, scratchpad)
    await publish_log_info(LogPrefix.USER, f"**************** Best next step prompt: {best_next_step_prompt}", __name__)

    # Call model to choose agent
    logger.info("#####  ~  Calling LLM for next best step  ~  #####")
    await publish_log_info(LogPrefix.USER, f"Scratchpad so far: {scratchpad}", __name__)
    best_next_step = await llm.chat(model, response_format_prompt, best_next_step_prompt, return_json=True)

    plan = to_json(best_next_step, "Failed to interpret LLM next step format from step string")
    await publish_log_info(LogPrefix.USER, f"Next best step response: {json.dumps(plan, indent=4)}", __name__)

    return plan


def find_agent_from_name(name):
    agents = get_available_agents()
    return (agent for agent in agents if agent.name == name)


async def get_agent_for_task(task, scratchpad) -> Agent | None:
    llm = get_llm(config.router_llm)
    model = config.router_model
    plan = await build_plan(task, llm, scratchpad, model)
    agent = next(find_agent_from_name(plan["agent_name"]), None)

    return agent
