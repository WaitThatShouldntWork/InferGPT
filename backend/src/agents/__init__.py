from src.utils import Config
from src.llm import get_llm
from .agent import Agent, agent
from .datastore_agent import DatastoreAgent
from .intent_agent import IntentAgent
from .maths_agent import MathsAgent
from .tool import tool, Parameter
from .validator_agent import ValidatorAgent
from .answer_agent import AnswerAgent

config = Config()

"""
    This module is being hit by certain tests, and for some reason the env variables in `test-backent.yml` are not being set
    So, two options:
        - get the env variables working in ci
        - separate this modul (There is a ticket for this...)
"""
print("HELLO - inside agents init. INTENT_AGENT_LLM = ", config.intent_agent_llm)
print("HELLO - inside agents init. MISTRAL_KEY = ", config.mistral_key)
print("HELLO - inside agents init. ANSWER_AGENT_LLM = ", config.answer_agent_llm)
print("HELLO - inside agents init. CONFIG = ", config)

validator_agent = ValidatorAgent(get_llm(config.validator_agent_llm))
intent_agent = IntentAgent(get_llm(config.intent_agent_llm))
answer_agent = AnswerAgent(get_llm(config.answer_agent_llm))


def get_agent_details(agent):
    return {"name": agent.name, "description": agent.description}


agents = [DatastoreAgent(get_llm(config.datastore_agent_llm)), MathsAgent(get_llm(config.maths_agent_llm))]
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
