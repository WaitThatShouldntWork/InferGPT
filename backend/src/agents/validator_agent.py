from src.utils import call_model
from src.agents import Agent, agent_metadata

validator_prompt = """
You are an expert validator. You can help with validating the answers to the tasks with just the information provided.

You're entire purpose is to return a boolean value to indicate if the answer has fulfilled the task.

You will be passed a task and an answer. You need to determine if the answer is correct or not.

e.g.
Task: What is 2 + 2?
Answer: 4
Response: True

Task: What is 2 + 2?
Answer: 5
Response: False

Task: Find all spending transactions last month on Amazon.
Answer: Last month you spend £64.21 on Amazon
Response: True

Task: Find all spending transactions last month on Amazon.
Answer: Last month you spend £64.21 on Spotify
Response: False
Reasoning: The answer is for Spotify not Amazon.

You must always return a single boolean value as the response, do not return any additional information, just the boolean value.
"""


@agent_metadata(
    name="ValidatorAgent",
    description="This agent is responsible for validating the answers to the tasks",
    prompt=validator_prompt,
    tools=[]
)
class ValidatorAgent(Agent):
    def invoke(self, utterance: str) -> str:
        return call_model(self.prompt, utterance)