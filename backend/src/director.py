import logging
from src.utils import call_model
from src.agents import create_tasks
from src.supervisors import solve_all_tasks

logging = logging.getLogger(__name__)

director_prompt = """
You are a Chat Bot called InferGPT.
Your sole purpose is to get the user to tell you their intention. The intention has to be specifically related
to the user. For example:
-spending
-personal interests

If the user does not provide an intention or the intention isn't directly related to the user,
attempt to provide an answer.
If you do not know the answer, do not try to make it up.

Eg.
An intention:
I want to save for a house
How much did I spend last month?

Not an intention:
How are you?
How many grams are there in an ounce?
"""

determine_intention_prompt = """
Your purpose is to determine whether the user prompt contains an intention that can be broken down into smaller tasks.
If the user prompt contains an intention return "TRUE". If it does not contain an intention return "FALSE".

Your reply should be one word only:
If goal:
TRUE
If no goal:
FALSE

If you reply more than one word, you will be disconnected
"""


def question(question):
    logging.debug("Received utterance: {question}")

    if determine_intention(question) == "TRUE":
        task_dict = create_tasks(question)
        final_answer = solve_all_tasks(task_dict)
        return final_answer

    logging.info("Passing utterance straight to call_model function")
    return call_model(director_prompt, user_prompt=question)


def determine_intention(question: str) -> str:
    logging.debug("director calling determine_intention function")
    return call_model(determine_intention_prompt, user_prompt=question)
