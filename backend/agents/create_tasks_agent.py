import json

from prompts.prompting import PromptEngine
from utils import Config
from utils import call_model
import logging

logger = logging.getLogger(__name__)
config = Config()
engine = PromptEngine()


def create_tasks(user_prompt: str) -> str:
    # TODO: Make single source of agent choice knowledge
    agents = "unresolvable_agent, database_agent, fiancial_advisor_agent, web_search_agent"

    create_tasks_prompt = engine.load_prompt("create-tasks", list_of_agents=agents)

    logger.debug("create_tasks function is called")
    response = call_model(create_tasks_prompt, user_prompt)

    try:
        all_tasks_json = json.loads(response)
    except Exception:
        raise Exception("Failed to interpret LLM next step format")

    logger.info("tasks created: " + str(all_tasks_json))
    return all_tasks_json
