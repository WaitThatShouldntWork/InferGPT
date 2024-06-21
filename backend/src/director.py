import json
import logging
from src.utils import clear_scratchpad, update_scratchpad
from src.agents import get_intent_agent, get_answer_agent
from src.prompts import PromptEngine
from src.supervisors import solve_all

logging = logging.getLogger(__name__)

engine = PromptEngine()
director_prompt = engine.load_prompt("director")


def question(question: str) -> str:
    logging.debug("Received utterance: {question}")
    intent = get_intent_agent().invoke(question)
    intent_json = json.loads(intent)
    logging.info(f"Intent determined: {intent}")

    try:
        solve_all(intent_json)
    except Exception as error:
        update_scratchpad(error=str(error))

    final_answer = get_answer_agent().invoke(question)
    logging.info(f"final answer: {final_answer}")

    clear_scratchpad()
    logging.info("scratchpad cleared")

    return final_answer
