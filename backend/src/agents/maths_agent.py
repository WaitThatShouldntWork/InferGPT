from .tool import tool_metadata
from .types import Parameter
from .agent import Agent, agent_metadata


@tool_metadata(
        name="sum list of values",
        description="sums a list of provided values",
        parameters={
            "list_of_values": Parameter(
            type="list[number]",
            description="Python list of comma separated values (e.g. [1, 5, 3])",
        )
    }
)
def sum_list_of_values(list_of_values) -> str:
    if not isinstance(list_of_values, list):
        raise Exception("Method not passed a valid Python list")
    return f"The sum of all the values passed {list_of_values} is {str(sum(list_of_values))}"


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
    tools=[sum_list_of_values, compare_two_values],
)
class MathsAgent(Agent):
    pass
