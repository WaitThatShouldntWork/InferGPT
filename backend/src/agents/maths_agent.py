from .tool import tool
from .agent_types import Parameter
from .agent import Agent, agent
import logging
from src.utils import Config
from .validator_agent import ValidatorAgent
import json
from src.utils.web_utils import perform_math_operation_util

logger = logging.getLogger(__name__)
config = Config()

# @tool(
#     name="sum list of values",
#     description="sums a list of provided values",
#     parameters={
#         "list_of_values": Parameter(
#             type="list[number]",
#             description="Python list of comma separated values (e.g. [1, 5, 3])",
#         )
#     },
# )
# async def sum_list_of_values(list_of_values) -> str:
#     if not isinstance(list_of_values, list):
#         raise Exception("Method not passed a valid Python list")
#     return f"The sum of all the values passed {list_of_values} is {str(sum(list_of_values))}"


# @tool(
#     name="compare two values",
#     description="Compare two passed values and return information on which one is greater",
#     parameters={
#         "thing_one": Parameter(
#             type="string",
#             description="first thing for comparison",
#         ),
#         "value_one": Parameter(
#             type="number",
#             description="value of first thing",
#         ),
#         "thing_two": Parameter(
#             type="string",
#             description="second thing for comparison",
#         ),
#         "value_two": Parameter(
#             type="number",
#             description="value of first thing",
#         ),
#     },
# )
# async def compare_two_values(value_one, thing_one, value_two, thing_two) -> str:
#     if value_one > value_two:
#         return f"You have spent more on {thing_one} ({value_one}) than {thing_two} ({value_two}) in the last month"
#     else:
#         return f"You have spent more on {thing_two} ({value_two}) than {thing_one} ({value_one}) in the last month"

# Core function to perform the math operation by calling the util function
async def perform_math_operation_core(math_query, llm, model) -> str:
    try:
        # Call the utility function to perform the math operation
        math_operation_result = await perform_math_operation_util(math_query, llm, model)
        result_json = json.loads(math_operation_result)

        if result_json.get("status") == "success":
            # Extract the relevant response (math result) from the utility function's output
            response = result_json.get("response", {})
            response_json = json.loads(response)
            result = response_json.get("result", "")
            # steps = response_json.get("steps", "")
            # reasoning = response_json.get("reasoning", "")

            if result:
                logger.info(f"Math operation successful: {result}")
                is_valid = await is_valid_answer(result, math_query)

                if is_valid:
                    response = {
                        "content": result,
                        "ignore_validation": "true"
                    }
                    return json.dumps(response, indent=4)
            else:
                response = {
                        "content": "No valid result found for the math query.",
                        "ignore_validation": "true"
                }
                return json.dumps(response, indent=4)
        else:
            response = {
                        "content": None,
                        "status": "error"
                    }
            return json.dumps(response, indent=4)
    except Exception as e:
        logger.error(f"Error in perform_math_operation_core: {e}")
        response = {
                    "content": None,
                    "status": "error"
                }
        return json.dumps(response, indent=4)

    # Ensure a return statement in all code paths
    response = {
                "content": None,
                "status": "error"
            }
    return json.dumps(response, indent=4)

def get_validator_agent() -> Agent:
    return ValidatorAgent(config.validator_agent_llm, config.validator_agent_model)

async def is_valid_answer(answer, task) -> bool:
    is_valid = (await get_validator_agent().invoke(f"Task: {task}  Answer: {answer}")).lower() == "true"
    return is_valid

# Math Operation Tool
@tool(
    name="perform_math_operation",
    description=(
        "Use this tool to perform complex mathematical operations or calculations. "
        "It can handle queries related to arithmetic operations, algebra, or calculations involving large numbers."
    ),
    parameters={
        "math_query": Parameter(
            type="string",
            description="The mathematical query or equation to solve."
        ),
    },
)
async def perform_math_operation(math_query, llm, model) -> str:
    return await perform_math_operation_core(math_query, llm, model)

# MathAgent definition
@agent(
    name="MathsAgent",
    description="This agent is responsible for handling mathematical queries and providing solutions.",
    tools=[perform_math_operation],
)
class MathsAgent(Agent):
    pass
