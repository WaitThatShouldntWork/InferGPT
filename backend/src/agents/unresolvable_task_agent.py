from .agent import Agent, agent_metadata

@agent_metadata(
    name="UnresolvableTaskAgent",
    description="This agent triggers the end of solving the overall problem if it cannot be solved",
    tools=[],
)
class UnresolvableTaskAgent(Agent):
    pass
