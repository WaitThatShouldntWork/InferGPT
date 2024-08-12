# src/llm/openai_llm.py
import logging
from .openai_client import OpenAIClient
from src.utils import Config
from .llm import LLM
from openai import NOT_GIVEN, AsyncOpenAI

logger = logging.getLogger(__name__)
config = Config()


class OpenAI(LLM):
    def __init__(self):
        self.client = OpenAIClient()

    async def chat(self, model, system_prompt: str, user_prompt: str, return_json=False) -> str:
        logger.debug(
            "##### Called open ai chat ... llm. Waiting on response model with prompt {0}.".format(
                str([system_prompt, user_prompt])
            )
        )
        client = AsyncOpenAI(api_key=config.openai_key)
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                response_format={"type": "json_object"} if return_json else NOT_GIVEN,
            )
            logger.info("OpenAI response: {0}".format(response))
            content = response.choices[0].message.content
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                return " ".join(content)
            else:
                return "Unexpected content format"
        except Exception as e:
            logger.error("Error calling OpenAI model: {0}".format(e))
            return "An error occurred while processing the request."
