from .create_tasks_agent import create_tasks
from .tool import tool, Parameter
from .agent import Agent, agent
from .datastore_agent import DatastoreAgent
from .maths_agent import MathsAgent
from .validator_agent import ValidatorAgent

validator_agent = ValidatorAgent()


def get_agent_details(agent):
    return {"name": agent.name, "description": agent.description}


agents = [DatastoreAgent(), MathsAgent()]
agents_details = [get_agent_details(agent) for agent in agents]

__all__ = [
    "Agent",
    "agents",
    "agents_details",
    "agent",
    "create_tasks",
    "tool",
    "Parameter",
    "validator_agent",
]
