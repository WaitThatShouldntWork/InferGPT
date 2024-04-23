import logging
from utils.llm import call_model
from agents.create_tasks_agent import create_tasks

logger = logging.getLogger(__name__)

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
    has_intent = determine_intention(question) == "TRUE"
    logger.info(f"intention identified: {has_intent}")
    if has_intent:
        return create_tasks(question)

    logger.info("director calling call_model function")
    return call_model(director_prompt, user_prompt=question)


def determine_intention(question):
    logger.info("director calling determine_intention function")
    return call_model(determine_intention_prompt, user_prompt=question)
