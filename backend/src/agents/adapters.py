from typing import List
from .tool import Parameter, Tool


def create_all_tools_str(tools: List[Tool]) -> str:
    return "".join(tool.to_str() + "\n\n" for tool in tools)


def extract_tool(chosen_tool_name: str, agent_tools: List[Tool]) -> Tool:
    if chosen_tool_name == "None":
        raise Exception("No tool deemed appropriate for task")
    try:
        tool = next(tool for tool in agent_tools if tool.name == chosen_tool_name)
    except Exception:
        raise Exception(f"Unable to find tool {chosen_tool_name} in available tools")
    return tool


def get_required_args(tool: Tool) -> dict[str, Parameter]:
    parameters_no_optional_args = tool.parameters.copy()
    for key, param in tool.parameters.items():
        if not param.required:
            parameters_no_optional_args.pop(key)
    return parameters_no_optional_args


def validate_args(chosen_tool_args: dict, defined_tool: Tool):
    # Get just the required arguments
    all_args_set = set(defined_tool.parameters.keys())
    required_args_set = set(get_required_args(defined_tool).keys())
    passed_args_set = set(chosen_tool_args.keys())

    if len(passed_args_set) > len(all_args_set):
        raise Exception(f"Unable to fit parameters {chosen_tool_args} to Tool arguments {all_args_set}: Extra params")

    if not required_args_set.issubset(passed_args_set):
        raise Exception(f"Unable to fit parameters {chosen_tool_args} to Tool arguments {all_args_set}: Wrong params")
