from typing import List

from src.agents.types import Action, Parameter
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
        "name": tool.action.__name__,
        "parameters": {
            key: {
                    "type": inner_dict.type,
                    "description": inner_dict.description,
                }
                for key, inner_dict in tool.parameters.items()
        },
    }

    return json.dumps(obj)


def extract_tool(chosen_tool: str, agent_tools: List[Tool]) -> Action:
    # new_tool = next((agent_tool for agent_tool in agent_tools if agent_tool.action.__name__ == chosen_tool.tool_name)
    return None


def extract_args(chosen_tool: str) -> List[Parameter]:
    return None
