# src/llm/openai_client.py
import openai
from src.utils import Config
import logging

config = Config()
logger = logging.getLogger(__name__)


class OpenAIClient:
    def __init__(self):
        self.api_key = config.openai_key
        openai.api_key = self.api_key

    def chat(self, model, messages, temperature=0, max_tokens=150):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
            )
            content = response["choices"][0]["message"]["content"]
            logger.debug(f'{model} response: "{content}"')
            return content
        except Exception as e:
            logger.error(f"Error calling OpenAI model: {e}")
            return "An error occurred while processing the request."
