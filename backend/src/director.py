import logging
from src.prompts import PromptEngine
from src.utils import call_model
from src.agents import create_tasks, agents_details
from src.supervisors import solve_all_tasks

logging = logging.getLogger(__name__)

engine = PromptEngine()
director_prompt = engine.load_prompt("director")
determine_intention_prompt = engine.load_prompt("determine-intention")

def question(question):
    logging.debug("Received utterance: {question}")

    if determine_intention(question) == "TRUE":
        task_dict = create_tasks(question, agents_details)
        final_answer = solve_all_tasks(task_dict)
        return final_answer

    logging.info("Passing utterance straight to call_model function")
    return call_model(director_prompt, user_prompt=question)


def determine_intention(question: str) -> str:
    logging.debug("director calling determine_intention function")
    return call_model(determine_intention_prompt, user_prompt=question)
