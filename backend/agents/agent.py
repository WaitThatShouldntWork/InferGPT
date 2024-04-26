from abc import ABC
from typing import List, Type
from utils import call_model_with_tools
from .adapters import get_mistral_tool
from .types import Action_and_args, Tool


class Agent(ABC):
    name: str
    description: str
    tools: List[Tool]
    prompt: str

    def get_action(self, utterance: str) -> Action_and_args:
        tools = map(get_mistral_tool, self.tools)
        (function_name, function_params) = call_model_with_tools(self.prompt, utterance, tools)

        function = next((tool for tool in self.tools if tool.action.__name__ == function_name), None)

        if function is None:
            raise ValueError(f"Tool {function_name} not found in agent {self.name}")

        return (function.action, function_params)

    def invoke(self, utterance: str) -> str:
        (action, args) = self.get_action(utterance)
        return action(**args)


def agent_metadata(name: str, description: str, prompt: str, tools: List[Tool]):
    def decorator(agent: Type[Agent]):
        agent.name = name
        agent.description = description
        agent.prompt = prompt
        agent.tools = tools
        return agent

    return decorator
