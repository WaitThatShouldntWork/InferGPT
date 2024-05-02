from agents import Agent, agent_metadata

@agent_metadata(
    name="UnresolvableTaskAgent",
    description="Pick this agent if you believe (based on the History of actions) you cannot solve the current task.",
    prompt="",
    tools=[],
)
class UnresolvableTaskAgent(Agent):
    pass
