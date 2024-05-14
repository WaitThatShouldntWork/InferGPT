import logging
from src.prompts import PromptEngine
from src.utils import call_model
from src.agents import Agent, agent_metadata

engine = PromptEngine()

validator_prompt = engine.load_prompt("validator")


@agent_metadata(
    name="ValidatorAgent",
    description="This agent is responsible for validating the answers to the tasks",
    prompt=validator_prompt,
    tools=[],
)
class ValidatorAgent(Agent):
    def invoke(self, utterance: str) -> str:
        answer = call_model(self.prompt, utterance)
        logging.info("Validator Agent:")
        logging.info(f"Utterance: '{utterance}' response: '{answer}'")

        return answer
