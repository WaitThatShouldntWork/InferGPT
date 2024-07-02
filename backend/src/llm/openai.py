from openai import OpenAI
import logging
from src.utils import Config
from .llm import LLM
logger = logging.getLogger(__name__)
config = Config()


class OpenAI(LLM):

    client = OpenAI(api_key=config.openai_key)
    def chat(self, system_prompt: str, user_prompt: str) -> str:
        logger.debug("##### Called open ai chat ... llm. Waiting on response model with prompt {0}."
                     .format(str([system_prompt,user_prompt])))

        try:
            response = self.client.chat.completions.create(
                model=config.openai_model,
                messages=[
                    {"role":"system", "content":system_prompt},
                    {"role":"user", "content":user_prompt},
                ],
                temperature=0,
                max_tokens=150,  # Adjust this value based on your requirements
            )
            content = response.choices[0].message.content

            logger.debug('{0} response : "{1}"'.format(config.openai_model, content))
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                return " ".join(content)
            else:
                return "Unexpected content format"


        except Exception as e:
            logger.error("Error calling OpenAI model: {0}".format(e))
            return "An error occurred while processing the request."
