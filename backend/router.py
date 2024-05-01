import json
import logging
from utils import get_response_three_prompts
from prompts.prompting import PromptEngine  # TODO: remove need for .prompting

# TODO: Create pick_agent test with mocked calls
prompt_engine = PromptEngine()


def convert_to_json(next_step):
    try:
        return json.loads(next_step)
    except Exception:
        raise Exception("Failed to interpret LLM next step format")

def pick_agent(task_string):
    logging.debug("Picking agent for task: " + task_string)

    list_of_agents = ["unresolvable_agent, database_agent, financial_advisor_agent, web_search_agent"]

    agent_list_prompt = prompt_engine.load_prompt("agents-list", list_of_agents=list_of_agents)
    response_format_prompt = prompt_engine.load_prompt("agent-selection-format")

    # TODO: Add previous successful step information (e.g. data retrieved from the agents)
    best_next_step_prompt = prompt_engine.load_prompt("task-step", task=task_string)

    # while 

    next_step = get_response_three_prompts(agent_list_prompt, response_format_prompt, best_next_step_prompt)

    logging.debug("Found next best step:")
    next_step_json = convert_to_json(next_step)
    logging.debug(next_step_json["thoughts"])

    return next_step_json["agent"]
