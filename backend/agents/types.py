from typing import Callable, Protocol, Tuple, TypeVar


Action = Callable[..., str]
T = TypeVar("T")
Action_and_args = Tuple[Action, T]

class Parameter:
    type: str
    description: str
    required: bool

    def __init__(self, type: str, description: str, required: bool = True):
        self.type = type
        self.description = description
        self.required = required


class Tool(Protocol):
    name: str
    description: str
    parameters: dict[str, Parameter]
    action: Action