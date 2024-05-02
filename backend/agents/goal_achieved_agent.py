from agents import Agent, agent_metadata

@agent_metadata(
    name="GoalAchievedAgent",
    description="Pick this agent if you believe you have solved BOTH the current task and the next task",
    prompt="",
    tools=[],
)
class GoalAchievedAgent(Agent):
    pass
