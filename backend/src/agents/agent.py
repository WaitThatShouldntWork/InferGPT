from abc import ABC
import json
import logging
from typing import List, Type
from src.llm import LLM, get_llm
from src.utils.log_publisher import LogPrefix, publish_log_info

from .adapters import create_all_tools_str, extract_tool, validate_args
from src.utils import get_scratchpad, Config
from src.prompts import PromptEngine
from .tool import Tool
from .types import Action_and_args

logger = logging.getLogger(__name__)
engine = PromptEngine()
format_prompt = engine.load_prompt("tool-selection-format")
config = Config()

class Agent(ABC):
    name: str
    description: str
    tools: List[Tool]
    llm: LLM
    model: str

    def __init__(self, llm_name: str | None, model: str):
        self.llm = get_llm(llm_name)
        self.model = model

    def __get_action(self, utterance: str) -> Action_and_args:

        tool_descriptions = create_all_tools_str(self.tools)

        tools_available = engine.load_prompt(
            "best-tool",
            task=utterance,
            scratchpad=get_scratchpad(),
            tools=tool_descriptions,
        )

        logger.debug(f"List of tools: {tool_descriptions}")
        response = json.loads(self.llm.chat(config.agent_class_model, format_prompt, tools_available))

        publish_log_info(LogPrefix.USER, f"Tool chosen: {json.dumps(response)}", __name__)

        try:
            chosen_tool = extract_tool(response["tool_name"], self.tools)
            chosen_tool_parameters = response["tool_parameters"]
            validate_args(chosen_tool_parameters, chosen_tool)
        except Exception:
            raise Exception(f"Unable to extract chosen tool and parameters from {response}")

        return (chosen_tool.action, chosen_tool_parameters)

    def invoke(self, utterance: str) -> str:
        (action, args) = self.__get_action(utterance)
        result_of_action = action(**args, llm=self.llm, model=self.model)
        publish_log_info(LogPrefix.USER, f"Action gave result: {result_of_action}", __name__)
        return result_of_action


def agent(name: str, description: str, tools: List[Tool]):
    def decorator(agent: Type[Agent]):
        agent.name = name
        agent.description = description
        agent.tools = tools
        return agent

    return decorator
