import logging
from src.prompts import PromptEngine
from src.utils import call_model
from src.agents import Agent, agent

logger = logging.getLogger(__name__)
engine = PromptEngine()
validator_prompt = engine.load_prompt("validator")


@agent(
    name="ValidatorAgent",
    description="This agent is responsible for validating the answers to the tasks",
    tools=[],
)
class ValidatorAgent(Agent):
    def invoke(self, utterance: str) -> str:
        answer = call_model(validator_prompt, utterance)
        logger.info(f"USER - Validating: '{utterance}' Answer: '{answer}'")

        return answer
