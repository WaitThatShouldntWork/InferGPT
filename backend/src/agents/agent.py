from abc import ABC
import json
import logging
from typing import List, Type
from src.agents.adapters import create_all_tools_str, extract_tool, extract_args, find_tool
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
        format_prompt = engine.load_prompt("tool-selection-format")
        tools_available = engine.load_prompt("best-tool", task=utterance, tools=create_all_tools_str(self.tools))
        logging.info("#################################tools_object_list_as_string#############################################")


        logging.info("#################################tools_available#############################################")
        logging.info(tools_available)

        response = json.loads(call_model(format_prompt, tools_available))
        logging.info("#####################################chosen_tool (by llm)###########################################")
        logging.info(response)

        chosen_tool = extract_tool(response, self.tools) # TODO: add logic for check
        chosen_args = extract_args(response) # TODO: add logic for check
        logging.info("#####################################tools validated and extracted###########################################")

        logging.info(chosen_tool)
        logging.info(chosen_args)

        # Find tool arguments

        return (chosen_tool, chosen_args)

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
