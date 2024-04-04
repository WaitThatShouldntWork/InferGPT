import logging
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from utils import Config

logger = logging.getLogger(__name__)
config = Config()

client = MistralClient(api_key=config.mlarge_key, endpoint=config.mlarge_url)

def call_model(system_prompt, user_prompt):
   logger.debug("call model " + model + " with prompt:\nsystem_prompt: " + system_prompt + "\nuser_prompt: " + user_prompt)
   response = client.chat(
      model=config.mlarge_model,
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
   logger.debug("response content received: " + response.choices[0].message.content)
   return response.choices[0].message.content
