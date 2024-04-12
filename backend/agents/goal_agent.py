import functools
import logging
from utils import Config
from utils import create_goal
from utils import call_model_with_tools

logger = logging.getLogger(__name__)
config = Config()

tools = [
    {
        "type": "function",
        "function": {
            "description": "Get a goal and its description from the user",
            "name": "create_goal",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "As a string, A single title keyword to summarise the goal eg. mortgage",
                    },
                    "description": {
                        "type": "string",
                        "description": "A string to summarise the goal",
                    },
                },
                "required": ["name", "description"],
            },
        },
    }
]

names_to_functions = {
    "create_goal": functools.partial(create_goal),
}

system_prompt = """
    You are an agent specifically designed to accomplish one task:
    extract a goal from a user's utterance and save it in the
    graph database.
    If the task is to do something other
    than extract a goal and save it
    reply saying that you are not able to do so.
    
    A goal should be saved as one or 2 words that extract the main purpose of the goal.
    
    EG. prompt: "I want to save for a house"
    goal: "House"
    description: "Save for a house"
    
    If you do not do this you will be disconnected.
"""


def create_user_goal(user_prompt):
    (function_name, function_params) = call_model_with_tools(
        system_prompt, user_prompt, tools
    )

    logger.info(
        "function_name: {0} function_params: {1}".format(function_name, function_params)
    )
    logger.info("Calling function: {0}".format(function_name))
    names_to_functions[function_name](**function_params)
    return function_params
