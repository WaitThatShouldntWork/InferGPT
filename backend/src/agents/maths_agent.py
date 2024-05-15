from .tool import tool_metadata
from .types import Parameter
from .agent import Agent, agent_metadata


@tool_metadata(
    name="compare two values",
    description="Compare two passed values and return information on which one is greater",
    parameters={
        "thing_one": Parameter(
            type="string",
            description="first thing for comparison",
        ),
        "value_one": Parameter(
            type="number",
            description="value of first thing",
        ),
        "thing_two": Parameter(
            type="string",
            description="second thing for comparison",
        ),
        "value_two": Parameter(
            type="number",
            description="value of first thing",
        ),
    },
)
def compare_two_values(value_one, thing_one, value_two, thing_two) -> str:
    if value_one > value_two:
        return f"You have spent more on {thing_one} ({value_one}) than {thing_two} ({value_two}) in the last month"
    else:
        return f"You have spent more on {thing_two} ({value_two}) than {thing_one} ({value_one}) in the last month"


@agent_metadata(
    name="MathsAgent",
    description="This agent is responsible for solving number comparison and calculation tasks",
    tools=[compare_two_values],
)
class MathsAgent(Agent):
    pass
