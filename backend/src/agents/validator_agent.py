import logging
from src.prompts import PromptEngine
from src.llm import call_model
from src.agents import Agent, agent

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
        logging.info("Validator Agent:")
        logging.info(f"Utterance: '{utterance}' response: '{answer}'")

        return answer
