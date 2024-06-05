from .agent import Agent, agent
from .create_tasks_agent import create_tasks
from .datastore_agent import DatastoreAgent
from .intent_agent import IntentAgent
from .maths_agent import MathsAgent
from .tool import tool, Parameter
from .validator_agent import ValidatorAgent
from .answer_agent import AnswerAgent

validator_agent = ValidatorAgent()
intent_agent = IntentAgent()
answer_agent = AnswerAgent()


def get_agent_details(agent):
    return {"name": agent.name, "description": agent.description}


agents = [DatastoreAgent(), MathsAgent()]
agents_details = [get_agent_details(agent) for agent in agents]

__all__ = [
    "agent",
    "Agent",
    "agents_details",
    "agents",
    "answer_agent",
    "create_tasks",
    "intent_agent",
    "Parameter",
    "tool",
    "validator_agent",
]
