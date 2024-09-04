import json
from typing import Callable
from .agent_types import Action, Parameter


class Tool:
    def __init__(self, name: str, description: str, parameters: dict[str, Parameter], action: Action):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.action = action

    def to_str(self) -> str:
        obj = {
            "description": self.description,
            "name": self.name,
            "parameters": {
                key: {
                    "type": inner_dict.type,
                    "description": inner_dict.description,
                }
                for key, inner_dict in self.parameters.items()
            },
        }
        return json.dumps(obj)


def tool(name: str, description: str, parameters: dict[str, Parameter]) -> Callable[[Action], Tool]:
    def create_tool_from(action: Action) -> Tool:
        return Tool(name, description, parameters, action)

    return create_tool_from
