import json

from src.prompts import PromptEngine
from src.utils import call_model, Config
import logging

logger = logging.getLogger(__name__)
config = Config()
engine = PromptEngine()

list_of_agents = [ "DatastoreAgent", "MathsAgent", "UnresolvableTaskAgent", "GoalAchievedAgent" ]

def create_tasks(user_prompt: str) -> str:

    create_tasks_prompt = engine.load_prompt("create-tasks", list_of_agents=list_of_agents)
    logger.info("create_tasks_prompt")
    logger.info(create_tasks_prompt)
    logger.info(f"Creating tasks from \"{user_prompt}\" user utterance...")
    response = call_model(create_tasks_prompt, user_prompt)

    try:
        all_tasks_json = json.loads(response)
    except Exception:
        raise Exception("Failed to interpret LLM next step format")

    logger.info("tasks created: " + json.dumps(all_tasks_json, indent=4))
    return all_tasks_json
