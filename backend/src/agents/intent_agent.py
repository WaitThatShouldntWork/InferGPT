from src.prompts import PromptEngine
from src.agents import Agent, agent

engine = PromptEngine()
intent_format = engine.load_prompt("intent-format")

@agent(
    name="IntentAgent",
    description="This agent is responsible for determining the intent of the user's utterance",
    tools=[],
)
class IntentAgent(Agent):

    def invoke(self, utterance: str) -> str:
        user_prompt = engine.load_prompt("intent", question=utterance)

        return self.llm.chat(self.model, intent_format, user_prompt=user_prompt)
