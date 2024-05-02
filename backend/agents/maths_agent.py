from .tool import tool_metadata
from .types import Parameter
from agents import Agent, agent_metadata


@tool_metadata(
    name="compare two values",
    description="Compare two passed values and return information on which one is greater",
    parameters={
        "value_one": Parameter(
            type="number",
            description="first value in comparison",
        ),
        "value_two": Parameter(
            type="number",
            description="second value in comparison",
        )
    },
)
def compare_two_values(value_one, value_two) -> str:
    return f"You have spent more on Amazon ({value_one}) than Netflix ({value_two}) in the last month"


maths_prompt = """
You are an expert mathematician. You can help with solving mathematical problems
"""


@agent_metadata(
    name="MathsAgent",
    description="This agent is responsible for solving number comparison and calculation tasks",
    prompt=maths_prompt,
    tools=[compare_two_values],
)
class MathsAgent(Agent):
    pass
