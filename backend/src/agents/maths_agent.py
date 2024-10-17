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
            if result:
                logger.info(f"Math operation successful: {result}")
                is_valid = await is_valid_answer(result, math_query)
                logger.info(f"Is the answer valid: {is_valid}")
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
        "It handles arithmetic operations and algebra, and also supports conversions to specific units like millions, rounding when necessary. "
        "Returns both the result and an explanation of the steps involved."
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
    description=(
        "This agent processes mathematical queries, performs calculations, and applies necessary formatting such as"
         "rounding or converting results into specific units (e.g., millions). "
        "It provides clear explanations of the steps involved to ensure accuracy."
    ),
    tools=[perform_math_operation],
)
class MathsAgent(Agent):
    pass
