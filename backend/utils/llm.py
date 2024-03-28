import os
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

load_dotenv()

try:
  endpoint = os.environ["INFER_GPT_MISTRAL_LARGE_ENDPOINT"]
  api_key = os.environ["INFER_GPT_MISTRAL_LARGE_KEY"]
  key = os.getenv("OPENAI_API_KEY")
  model = "azureai" # might me mistral-large

  client = MistralClient(api_key=api_key, endpoint=endpoint)
except FileNotFoundError:
   raise FileNotFoundError("Please provide a .env file. See the Getting Started guide on the README.md")
except:
   raise Exception("Missing .env file property. See the Getting Started guide on the README.md")

def call_model(prompt):
   response = client.chat(
      model=model,
      messages=[
         ChatMessage(
            role="user",
            content=prompt
         )
      ],
      max_tokens=125
   )
   print(response.choices[0].message.content)
   return response.choices[0].message.content
