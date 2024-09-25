from .tool import tool
from .agent_types import Parameter
from .agent import Agent, agent


@tool(
    name="sum list of values",
    description="sums a list of provided values",
    parameters={
        "list_of_values": Parameter(
            type="list[number]",
            description="Python list of comma separated values (e.g. [1, 5, 3])",
        )
    },
)
async def sum_list_of_values(list_of_values) -> str:
    if not isinstance(list_of_values, list):
        raise Exception("Method not passed a valid Python list")
    return f"The sum of all the values passed {list_of_values} is {str(sum(list_of_values))}"


@tool(
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
async def compare_two_values(value_one, thing_one, value_two, thing_two) -> str:
    if value_one > value_two:
        return f"You have spent more on {thing_one} ({value_one}) than {thing_two} ({value_two}) in the last month"
    else:
        return f"You have spent more on {thing_two} ({value_two}) than {thing_one} ({value_one}) in the last month"


@tool(
    name="round a number",
    description="Rounds a provided number to the specified number of decimal places",
    parameters={
        "number": Parameter(
            type="number",
            description="The number to round off",
        ),
        "decimal_places": Parameter(
            type="number",
            description="The number of decimal places to round to (e.g. 2)",
        ),
    },
)
async def round_number(number, decimal_places) -> str:
    return f"The number {number} rounded to {decimal_places} decimal places is {round(number, decimal_places)}"

@tool(
    name="find maximum value",
    description="Finds the maximum value in a provided list",
    parameters={
        "list_of_values": Parameter(
            type="list[number]",
            description="Python list of comma-separated values (e.g. [1, 5, 3])",
        ),
    },
)
async def find_max_value(list_of_values) -> str:
    if not isinstance(list_of_values, list):
        raise Exception("Method not passed a valid Python list")
    return f"The maximum value in the list {list_of_values} is {max(list_of_values)}"

@tool(
    name="find minimum value",
    description="Finds the minimum value in a provided list",
    parameters={
        "list_of_values": Parameter(
            type="list[number]",
            description="Python list of comma-separated values (e.g. [1, 5, 3])",
        ),
    },
)
async def find_min_value(list_of_values) -> str:
    if not isinstance(list_of_values, list):
        raise Exception("Method not passed a valid Python list")
    return f"The minimum value in the list {list_of_values} is {min(list_of_values)}"

@agent(
    name="MathsAgent",
    description="This agent is responsible for solving number comparison and calculation tasks",
    tools=[sum_list_of_values, compare_two_values, round_number, find_max_value, find_min_value],
)
class MathsAgent(Agent):
    pass
