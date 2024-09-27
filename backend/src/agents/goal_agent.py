from .agent import Agent, agent
from .tool import tool
from .agent_types import Parameter
from src.prompts import PromptEngine
from src.llm.llm import LLM
import logging
import json

engine = PromptEngine()
logger = logging.getLogger(__name__)

async def create_goal_core(goal_query, llm: LLM, model) -> str:
    goal_prompt = engine.load_prompt("goal-agent", utterance=goal_query)
    llm_response = await llm.chat(model, goal_query, goal_prompt, return_json=True)
    logger.info(f"goal from llm {llm_response}")
    response = {
        "content": llm_response,
        "ignore_validation": "false"
    }
    return json.dumps(response, indent=4)

@tool(
    name="create a goal",
    description="Create a goal if the user utterance contains one",
    parameters={
        "goal_query": Parameter(
            type="string",
            description="A goal set by the user",
        )
    },
)

async def create_goal(goal_query, llm: LLM, model) -> str:
    return await create_goal_core(goal_query, llm, model)

@agent(
    name="GoalAgent",
    description="This agent is responsible for creating a goal.",
    tools=[create_goal],
)
class GoalAgent(Agent):
    pass
