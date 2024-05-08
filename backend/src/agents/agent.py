from abc import ABC
import logging
from typing import List, Type
from src.utils import call_model
from src.prompts import PromptEngine
from .adapters import convert_to_mistral_tool
from .tool import Tool
from .types import Action_and_args

engine = PromptEngine()

class Agent(ABC):
    name: str
    description: str
    tools: List[Tool]

    def __get_action(self, utterance: str) -> Action_and_args:
        tools = map(convert_to_mistral_tool, self.tools)
        (function_name, function_params) = call_model(
            engine.load_prompt("tool-selection-format"),
            engine.load_prompt("best-tool", task=utterance, tools=tools)
        )

        tool = next((tool for tool in self.tools if tool.action.__name__ == function_name), None)

        if tool is None:
            raise ValueError(f"Tool {function_name} not found in agent {self.name}")

        return (tool.action, function_params)

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
