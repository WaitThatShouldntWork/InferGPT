import os
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

load_dotenv()

try:
  endpoint = os.environ["INFER_GPT_MISTRAL_LARGE_ENDPOINT"]
  api_key = os.environ["INFER_GPT_MISTRAL_LARGE_KEY"]
  model = os.environ["INFER_GPT_MODEL"]# might me mistral-large

  client = MistralClient(api_key=api_key, endpoint=endpoint)
except FileNotFoundError:
   raise FileNotFoundError("Please provide a .env file. See the Getting Started guide on the README.md")
except:
   raise Exception("Missing .env file property. See the Getting Started guide on the README.md")

def call_model(system_prompt, user_prompt):
   response = client.chat(
      model=model,
      messages=[
         ChatMessage(
            role="system",
            content=system_prompt
         ),
         ChatMessage(
            role="user",
            content=user_prompt
         )
      ],
      max_tokens=125
   )
   return response.choices[0].message.content
