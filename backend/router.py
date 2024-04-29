import json
import logging
from utils import get_response_three_prompts
from prompts.prompting import PromptEngine # TODO: remove need for .prompting

# TODO: Create pick_agent test with mocked calls

def pick_agent(task_string):
    logging.debug("Picking agent for task: " + task_string)

    prompt_engine = PromptEngine()
    list_of_agents = ["DatastoreRetrievalAgent, FinancialAssistantAgent, GoalAgent"]

    agent_list_prompt = prompt_engine.load_prompt("agents-list", list_of_agents=list_of_agents)
    response_format_prompt = prompt_engine.load_prompt("agent-selection-format")
    best_next_step_prompt = prompt_engine.load_prompt("task-step", task=task_string)

    next_step = get_response_three_prompts(agent_list_prompt, response_format_prompt, best_next_step_prompt)

    # collect all required prompts
        # system-prompt: List of agents that can be called
        # system-prompt: Expected response shape (probably a json)
        # user-prompt: "pick an agent and fit to the response shape to solve {taskString}

    logging.debug("Found next best step:")

    try:
        next_step_json = json.loads(next_step)
    except Exception:
        raise Exception("Failed to interpret LLM next step format")

    logging.debug(next_step_json["thoughts"])

    return next_step_json
