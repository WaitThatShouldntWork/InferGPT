from .agent import Agent, agent_metadata

@agent_metadata(
    name="GoalAchievedAgent",
    prompt="",
    description="Pick this agent if you believe you have solved BOTH the Current Task and the Next Task",
    tools=[],
)
class GoalAchievedAgent(Agent):
    pass
