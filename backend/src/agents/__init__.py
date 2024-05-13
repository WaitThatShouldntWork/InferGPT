from .create_tasks_agent import create_tasks
from .tool import tool_metadata, Parameter
from .agent import Agent, agent_metadata, convert_to_mistral_tool
from .datastore_agent import DatastoreAgent
from .maths_agent import MathsAgent
from .validator_agent import ValidatorAgent

validator_agent = ValidatorAgent()

def get_agent_details(agent):
    return {
        "name": agent.name,
        "description": agent.description
    }

agents = [ DatastoreAgent(), MathsAgent() ]
agents_details = [get_agent_details(agent) for agent in agents]

__all__ = ["Agent", "agents", "agents_details", "agent_metadata",
           "create_tasks", "tool_metadata", "Parameter", "convert_to_mistral_tool", "validator_agent"]
