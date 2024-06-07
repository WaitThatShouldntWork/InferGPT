import json
import logging
from src.utils.scratchpad import clear_scratchpad
from src.agents import intent_agent, answer_agent
from src.prompts import PromptEngine
from src.utils import call_model
from src.supervisors import solve_all

logging = logging.getLogger(__name__)

engine = PromptEngine()
director_prompt = engine.load_prompt("director")
determine_intention_prompt = engine.load_prompt("determine-intention")


def question(question):
    logging.debug("Received utterance: {question}")
    intent = intent_agent.invoke(question)
    intent_json = json.loads(intent)
    logging.info(f"Intent determined: {intent}")

    final_scratchpad = solve_all(intent_json)
    final_answer = answer_agent.invoke(question, final_scratchpad)
    logging.info(f"final answer: {final_answer}")

    clear_scratchpad()
    logging.info("scratchpad cleared")

    return final_answer


def determine_intention(question: str) -> str:
    logging.debug("director calling determine_intention function")
    return call_model(determine_intention_prompt, user_prompt=question)
