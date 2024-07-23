from typing import Any, Callable, Coroutine, Tuple, TypeVar


Action = Callable[..., Coroutine[Any, Any, str]]
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
