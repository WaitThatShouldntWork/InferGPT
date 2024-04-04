import logging
from utils.llm import call_model

logger = logging.getLogger(__name__)

system_prompt= """
You are a Chat Bot called InferGPT.
You're abilities include:
- Setting and tracking Goals
"""

def question(question):
  logger.info("director calling call_model method")
  return call_model(system_prompt, user_prompt=question)
