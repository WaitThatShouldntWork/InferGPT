from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from backend.config import Config

config = Config()

client = MistralClient(api_key=config.mlarge_key, endpoint=config.url)

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
