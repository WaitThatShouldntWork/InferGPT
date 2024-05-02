from .types import Parameter, Tool


def tool_metadata(name: str, description: str, parameters: dict[str, Parameter]):
    def decorator(tool) -> Tool:
        tool.name = name
        tool.description = description
        tool.parameters = parameters
        tool.action = tool

        return tool

    return decorator
