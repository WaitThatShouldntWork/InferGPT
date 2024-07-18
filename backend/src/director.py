import json
import logging
from src.utils import clear_scratchpad, update_scratchpad
from src.agents import get_intent_agent, get_answer_agent
from src.prompts import PromptEngine
from src.supervisors import solve_all
from src.utils import Config
from src.agents.web_agent import WebAgent

logger = logging.getLogger(__name__)
config = Config()
engine = PromptEngine()
director_prompt = engine.load_prompt("director")

# Create an instance of the WebAgent
web_agent = WebAgent(config.web_agent_llm, config.web_agent_model)

def question(question: str) -> str:
    intent = get_intent_agent().invoke(question)
    intent_json = json.loads(intent)
    logger.info(f"Intent determined: {intent}")

    try:
        solve_all(intent_json)
    except Exception as error:
        logger.error(f"Error during task solving: {error}")
        update_scratchpad(error=str(error))

    final_answer = get_answer_agent().invoke(question)
    logger.info(f"final answer: {final_answer}")

    clear_scratchpad()

    return final_answer
