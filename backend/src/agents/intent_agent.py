from src.prompts import PromptEngine
from src.agents import Agent, agent
import logging
import os
import json
from src.utils.config import Config


config = Config()

engine = PromptEngine()
intent_format = engine.load_prompt("intent-format")
logger = logging.getLogger(__name__)
FILES_DIRECTORY = f"/app/{config.files_directory}"

# Constants for response status
IGNORE_VALIDATION = "true"
STATUS_SUCCESS = "success"
STATUS_ERROR = "error"

@agent(
    name="IntentAgent",
    description="This agent is responsible for determining the intent of the user's utterance",
    tools=[],
)
class IntentAgent(Agent):

    async def read_file_core(self, file_path: str) -> str:
        full_path = os.path.normpath(os.path.join(FILES_DIRECTORY, file_path))
        try:
            with open(full_path, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            error_message = f"File {file_path} not found."
            logger.error(error_message)
            return ""
        except Exception as e:
            logger.error(f"Error reading file {full_path}: {e}")
            return ""

    async def invoke(self, utterance: str) -> str:
        chat_history = await self.read_file_core("conversation-history.txt")

        user_prompt = engine.load_prompt("intent", question=utterance, chat_history=chat_history)

        return await self.llm.chat(self.model, intent_format, user_prompt=user_prompt, return_json=True)


    # Utility function for error responses
def create_response(content: str, status: str = STATUS_SUCCESS) -> str:
    return json.dumps({
        "content": content,
        "ignore_validation": IGNORE_VALIDATION,
        "status": status
    }, indent=4)
