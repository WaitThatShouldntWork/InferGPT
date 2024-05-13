from src.agents import Agent, agent_metadata

mock_agent_description = "A test agent"
mock_agent_name = "Mock Agent"
mock_prompt = "You are a bot!"
mock_tools = []


@agent_metadata(name=mock_agent_name, description=mock_agent_description, prompt=mock_prompt, tools=mock_tools)
class MockAgent(Agent):
    pass


__all__ = ["MockAgent", "mock_agent_description", "mock_agent_name", "mock_prompt", "mock_tools"]
