from datetime import datetime
from typing import Optional
from src.utils import call_model
from src.prompts import PromptEngine
from src.agents import Agent, agent

engine = PromptEngine()


@agent(
    name="AnswerAgent",
    description="This agent is responsible for generating an answer for the user, based on results in the scratchpad",
    tools=[],
)
class AnswerAgent(Agent):
    def invoke(self, question: str, final_scratchpad: Optional[str] = None) -> str:
        create_answer = engine.load_prompt("create_answer", final_scratchpad=final_scratchpad, datetime=datetime.now())

        return call_model(create_answer, user_prompt=question)
