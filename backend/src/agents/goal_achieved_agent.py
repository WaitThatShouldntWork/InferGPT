from .agent import Agent, agent_metadata

@agent_metadata(
    name="GoalAchievedAgent",
    description="This agent triggers the end of solving the overall problem and returns the final answer to the user",
    tools=[],
)
class GoalAchievedAgent(Agent):
    pass
