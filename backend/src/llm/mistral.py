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
        if response is None:
            logger.error("Call to mistral api failed: response was None")
            return "An error occurred while processing the request."

        if response.choices is None:
            logger.error("Call to mistral api failed: response.choices was None")
            return "An error occurred while processing the request."

        if len(response.choices) < 1:
            logger.error("Call to mistral api failed: response.choices was empty")
            return "An error occurred while processing the request."

        logger.debug('{0} response : "{1}"'.format(model, response.choices[0].message.content))

        content = response.choices[0].message.content
        if isinstance(content, str):
            return content
        else:
            logger.error("Call to mistral api failed: message.content was None or Unset")
            return "An error occurred while processing the request."
