from abc import ABC
import json
import logging
from typing import List, Type
from .adapters import create_all_tools_str, extract_tool
from src.utils import call_model
from src.prompts import PromptEngine
from .tool import Tool
from .types import Action_and_args

engine = PromptEngine()

class Agent(ABC):
    name: str
    description: str
    tools: List[Tool]
    # TODO: Test method
    def __get_action(self, utterance: str) -> Action_and_args:
        # TODO: refine logging
        format_prompt = engine.load_prompt("tool-selection-format")
        tools_available = engine.load_prompt("best-tool", task=utterance, tools=create_all_tools_str(self.tools))

        logging.info("#################################tools_available#############################################")
        logging.info(tools_available)

        response = json.loads(call_model(format_prompt, tools_available))
        try:
            tool_name = response["tool_name"]
            tool_parameters = response["tool_parameters"]
        except Exception:
            raise Exception(f"Unable to extract tool name and parameters from {response}")
        logging.info("#####################################chosen_tool (by llm)####################################")
        logging.info(response)
        logging.info(tool_name)
        logging.info(tool_parameters)

        chosen_tool = extract_tool(tool_name, self.tools) # TODO: add logic for check
        # chosen_args = extract_args(tool_parameters) # TODO: add logic for check
        logging.info("#####################################tools validated and extracted###########################")

        logging.info(chosen_tool)
        logging.info(tool_parameters)

        # Find tool arguments

        return (chosen_tool, tool_parameters)

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
