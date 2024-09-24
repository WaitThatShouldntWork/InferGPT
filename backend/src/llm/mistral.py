from mistralai import Mistral as MistralApi, UserMessage, SystemMessage
import logging
from src.utils import Config
from .llm import LLM

logger = logging.getLogger(__name__)
config = Config()


class Mistral(LLM):
    client = MistralApi(api_key=config.mistral_key)

    async def chat(self, model, system_prompt: str, user_prompt: str, return_json=False) -> str:
        logger.debug("Called llm. Waiting on response model with prompt {0}.".format(str([system_prompt, user_prompt])))
        response = await self.client.chat.complete_async(
            model=model,
            messages=[
                SystemMessage(content=system_prompt),
                UserMessage(content=user_prompt),
            ],
            temperature=0,
            response_format={"type": "json_object"} if return_json else None,
        )
        if not response or not response.choices:
            logger.error("Call to Mistral API failed: No valid response or choices received")
            return "An error occurred while processing the request."

        content = response.choices[0].message.content
        if not content:
            logger.error("Call to Mistral API failed: message content is None or Unset")
            return "An error occurred while processing the request."

        logger.debug('{0} response : "{1}"'.format(model, response.choices[0].message.content))
        return content
