from utils.llm import call_model

prompt= """
You are a Chat Bot called InferGPT.

You're abilities include:

- Setting and tracking Goals
- Remembering conversation information from previous sessions and using it in future discussions

Introduce yourself if asked.
"""

def question(question):

  prompt_with_question = prompt + "\n\nAnswer the following question: " + question

  return call_model(prompt_with_question)
