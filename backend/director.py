import logging
from utils.llm import call_model
from agents.goal_agent import create_user_goal

logger = logging.getLogger(__name__)

system_prompt= """
You are a Chat Bot called InferGPT.
Your sole purpose is to get the user to tell you their goal.
If the user does not provide a goal, ask them to provide a goal 
"""

system_prompt_to_determine_intent= """
Your purpose is to determine whether the user prompt contains a goal. If the user prompt contains a goal return "TRUE". If it does not contain a goal return "FALSE".

Your reply should be one word only:
If goal:
TRUE
If no goal:
FALSE

If you reply more than one word, you will be disconnected
"""

def question(question):
  logger.info("director calling call_model method")
  response = determine_intent(question)
  if response == "FALSE":
    return call_model(system_prompt, user_prompt=question)
  else: 
    goal_saved = create_user_goal(question)
    return "I have created a goal for you. Goal: {0}. Description: {1}".format(goal_saved['name'], goal_saved['description'])

def determine_intent(question):
  return call_model(system_prompt_to_determine_intent, user_prompt=question)
