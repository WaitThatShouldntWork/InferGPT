from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatCompletionResponse, ChatMessage
import logging
from src.utils import Config
from .llm import LLM

logger = logging.getLogger(__name__)
config = Config()


class Mistral(LLM):
    client = MistralClient(api_key=config.mistral_key)

    def chat(self, model, system_prompt: str, user_prompt: str, return_json=False) -> str:
        logger.debug("Called llm. Waiting on response model with prompt {0}.".format(str([system_prompt, user_prompt])))
        response: ChatCompletionResponse = self.client.chat(
            model=model,
            messages=[
                ChatMessage(role="system", content=system_prompt),
                ChatMessage(role="user", content=user_prompt),
            ],
            temperature=0,
            response_format={"type": "json_object"} if return_json else None,
        )
        logger.debug('{0} response : "{1}"'.format(model, response.choices[0].message.content))

        content = response.choices[0].message.content

        return content if isinstance(content, str) else " ".join(content)
