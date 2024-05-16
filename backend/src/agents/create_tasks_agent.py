import json
import logging

from src.prompts import PromptEngine
from src.utils import call_model, Config, to_json

logger = logging.getLogger(__name__)
config = Config()
engine = PromptEngine()


def create_tasks(user_prompt: str, agents_details: list[dict[str, str]]) -> str:
    create_tasks_prompt = engine.load_prompt("create-tasks", list_of_agents=agents_details)
    logger.info(f'Creating tasks from "{user_prompt}" user utterance...')
    response = call_model(create_tasks_prompt, user_prompt)

    tasks_dict = to_json(response, "Failed to interpret LLM next step format")

    logger.info("tasks created: " + json.dumps(tasks_dict, indent=4))
    return tasks_dict
