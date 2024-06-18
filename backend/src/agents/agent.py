from abc import ABC
import json
import logging
from typing import List, Type
from src.llm import LLM, get_llm

from .adapters import create_all_tools_str, extract_tool, validate_args
from src.utils import get_scratchpad
from src.prompts import PromptEngine
from .tool import Tool
from .types import Action_and_args

engine = PromptEngine()
format_prompt = engine.load_prompt("tool-selection-format")


class Agent(ABC):
    name: str
    description: str
    tools: List[Tool]
    llm: LLM

    def __init__(self, llm_name: str | None):
        self.llm = get_llm(llm_name)

    def __get_action(self, utterance: str) -> Action_and_args:
        tools_available = engine.load_prompt(
            "best-tool",
            task=utterance,
            scratchpad=get_scratchpad(),
            tools=create_all_tools_str(self.tools),
        )

        logging.info("#####  ~  Picking Action from tools:  ~  #####")
        logging.info(create_all_tools_str(self.tools))

        response = json.loads(self.llm.chat(format_prompt, tools_available))

        logging.info("Tool chosen - choice response:")
        logging.info(json.dumps(response))

        try:
            chosen_tool = extract_tool(response["tool_name"], self.tools)
            chosen_tool_parameters = response["tool_parameters"]
            validate_args(chosen_tool_parameters, chosen_tool)
        except Exception:
            raise Exception(f"Unable to extract chosen tool and parameters from {response}")

        return (chosen_tool.action, chosen_tool_parameters)

    def invoke(self, utterance: str) -> str:
        (action, args) = self.__get_action(utterance)
        result_of_action = action(**args, llm=self.llm)
        logging.info(f"Action gave result: {result_of_action}")
        return result_of_action


def agent(name: str, description: str, tools: List[Tool]):
    def decorator(agent: Type[Agent]):
        agent.name = name
        agent.description = description
        agent.tools = tools
        return agent

    return decorator
