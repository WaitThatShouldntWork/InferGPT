from typing import List

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


def extract_tool(chosen_tool_name: str, agent_tools: List[Tool]) -> Tool:
    if chosen_tool_name == "None":
        raise Exception("No tool deemed appropriate for task")
    try:
        tool = next(tool for tool in agent_tools if tool.name == chosen_tool_name)
    except Exception:
        raise Exception(f"Unable to find tool {chosen_tool_name} in available tools")
    return tool


def validate_args(chosen_tool_args: dict, tool: Tool):
    if tool.parameters.keys() != chosen_tool_args.keys():
        raise Exception(f"Unable to fit parameters {chosen_tool_args} to Tool arguments {str(tool.parameters.keys())}")
