from src.utils import Config
from .agent import Agent, agent
from .datastore_agent import DatastoreAgent
from .intent_agent import IntentAgent
from .maths_agent import MathsAgent
from .tool import tool, Parameter
from .validator_agent import ValidatorAgent
from .answer_agent import AnswerAgent

config = Config()


validator_agent = ValidatorAgent(config.validator_agent_llm)
intent_agent = IntentAgent(config.intent_agent_llm)
answer_agent = AnswerAgent(config.answer_agent_llm)


def get_agent_details(agent):
    return {"name": agent.name, "description": agent.description}


agents = [DatastoreAgent(config.datastore_agent_llm), MathsAgent(config.maths_agent_llm)]
agents_details = [get_agent_details(agent) for agent in agents]

__all__ = [
    "agent",
    "Agent",
    "agents_details",
    "agents",
    "answer_agent",
    "intent_agent",
    "Parameter",
    "tool",
    "validator_agent",
]
