from typing import List

from src.agents.types import Action
from .tool import Tool
import json
import logging

def create_all_tools_str(tools: List[Tool]) -> str:
    tools_object_list_as_string = ""
    for tool in tools:
        tools_object_list_as_string += to_object(tool) + "\n\n"
    logging.info(tools_object_list_as_string)
    return tools_object_list_as_string


def to_object(tool: Tool) -> str:
    obj = {
        "description": tool.description,
        "name": tool.name,
        "parameters": {
            key: {
                    "type": inner_dict.type,
                    "description": inner_dict.description,
                }
                for key, inner_dict in tool.parameters.items()
        },
    }

    return json.dumps(obj)



def extract_tool(chosen_tool_name: str, agent_tools: List[Tool]) -> Action:
    try:
        tool = next(tool.action for tool in agent_tools if tool.name == chosen_tool_name)
    except Exception:
        raise Exception(f"Unable to fit tool {chosen_tool_name}")
    return tool

# TODO: Test method
def extract_args(chosen_tool_args: dict) -> dict:
    parameters_dict = {}
    try:
        # fit to object
        for name, value in chosen_tool_args:
            parameters_dict[name] = value
    except Exception:
        raise Exception(f"Unable to fit parameters {chosen_tool_args}")

    return parameters_dict
