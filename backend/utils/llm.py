import logging
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from utils import Config

logger = logging.getLogger(__name__)
config = Config()

client = MistralClient(api_key=config.mistral_key)

def call_model(system_prompt, user_prompt):
   logger.info("called llm. Waiting on response model with prompt {0}".format(str([system_prompt, user_prompt])))
   response = client.chat(
      model=config.mistral_model,
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
   logger.info("{0} response : \"{1}\"".format(config.mlarge_model, response.choices[0].message.content))
   return response.choices[0].message.content
