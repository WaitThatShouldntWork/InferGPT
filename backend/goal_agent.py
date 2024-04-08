import functools
import logging
import json
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from utils import Config
from utils import graph_db_utils

logger = logging.getLogger(__name__)
config = Config()

client = MistralClient(api_key=config.mistral_key)

tools = [
    {
        "type": "function",
        "function": {
            "description": "Get a goal and its description from the user",
            "name": "create_goal",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal_name": {
                        "type": "string",
                        "description": "As a string, A single title keyword to summarise the goal eg. mortgage",
                    },
                    "goal_description": {
                        "type": "string",
                        "description": "A string to summarise the goal",
                    },
                },
                "required": ["title"],
            },
        },
    }
]
 
names_to_functions = {
    'create_goal': functools.partial(graph_db_utils.create_goal),
}
 
agent_system_message = """
    You are an agent specifically designed to accomplish one task:  
    extract a goal from a user's utterance and save it in the
    graph database.
    If the task is to do something other
    than extract a goal and save it
    reply saying that you are not able to do so.
"""
user_prompt = "I want to save for a house in 5 years time"
 
messages=[
        ChatMessage(
            role="system",
            content=agent_system_message
        ),
        ChatMessage(
            role="user",
            content=user_prompt
        )
    ]

response = client.chat(model=config.mistral_model, messages=messages, tools=tools, tool_choice="any")
 
print(response.choices[0])

tool_call = response.choices[0].message.tool_calls[0]
function_name = tool_call.function.name
function_params = json.loads(tool_call.function.arguments)
print("\nfunction_name: ", function_name, "\nfunction_params: ", function_params)

names_to_functions[function_name](**function_params)
