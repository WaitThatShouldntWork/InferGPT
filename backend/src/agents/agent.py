from abc import ABC
import json
import logging
from typing import List, Type
from src.agents.adapters import to_object
from src.utils import call_model
from src.prompts import PromptEngine
from .tool import Tool
from .types import Action_and_args

engine = PromptEngine()

class Agent(ABC):
    name: str
    description: str
    tools: List[Tool]

    def __get_action(self, utterance: str) -> Action_and_args:
        tools_object_list = []
        for tool in self.tools:
            tools_object_list.append(to_object(tool))
        logging.info("################################tools_object_list###########################################")
        logging.info(tools_object_list)
        tools_object_list_as_string = ""
        for tool_object in tools_object_list:
            tools_object_list_as_string += tool_object + "\n\n"
        logging.info("#################################tools_object_list_as_string#############################################")
        logging.info(tools_object_list_as_string)

        format_prompt = engine.load_prompt("tool-selection-format")
        tools_available = engine.load_prompt("best-tool", task=utterance, tools=tools_object_list_as_string)

        logging.info("#################################tools_available#############################################")
        logging.info(tools_available)

        chosen_tool = json.loads(call_model(format_prompt, tools_available))
        logging.info("#####################################chosen_tool (by llm)###########################################")
        logging.info(chosen_tool)

        if (chosen_tool.)

        logging.info("#####################################tool_validated###########################################")

        tool = next((tool for tool in self.tools if tool.action.__name__ == chosen_tool["tool_name"]), None)


        logging.info("#####################################tool (from real tools list)###########################################")
        logging.info(tool)

        if tool is None:
            raise ValueError(f"Tool {chosen_tool.tool_name} not found in agent {self.name}")
        
        # Find tool arguments
        chosen_tool

        return (tool.action, chosen_tool["tool_parameters"])

    def invoke(self, utterance: str) -> str:
        (action, args) = self.__get_action(utterance)
        result_of_action = action(**args)
        logging.info(f"Tool \"{action.name}\" chosen for agent \"{self.name}\" with result: {result_of_action}")
        return result_of_action


def agent_metadata(name: str, description: str, tools: List[Tool]):
    def decorator(agent: Type[Agent]):
        agent.name = name
        agent.description = description
        agent.tools = tools
        return agent

    return decorator
