import logging
from src.prompts import PromptEngine
from src.agents import Agent, agent
from src.utils.log_publisher import LogPrefix, publish_log_info

logger = logging.getLogger(__name__)
engine = PromptEngine()
validator_prompt = engine.load_prompt("validator")


@agent(
    name="ValidatorAgent",
    description="This agent is responsible for validating the answers to the tasks",
    tools=[],
)
class ValidatorAgent(Agent):
    async def invoke(self, utterance: str) -> str:
        answer = await self.llm.chat(self.model, validator_prompt, utterance)
        publish_log_info(LogPrefix.USER, f"Validating: '{utterance}' Answer: '{answer}'", __name__)

        return answer
