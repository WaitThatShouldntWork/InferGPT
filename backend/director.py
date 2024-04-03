from utils.llm import call_model

system_prompt= """
You are a Chat Bot called InferGPT.
You're abilities include:
- Setting and tracking Goals
- Remembering conversation information from previous sessions and using it in future discussions
"""

def question(question):
  return call_model(system_prompt, user_prompt=question)
