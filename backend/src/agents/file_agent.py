import logging
from .agent_types import Parameter
from .agent import Agent, agent
from .tool import tool
import json
import os
from src.utils.config import Config

logger = logging.getLogger(__name__)
config = Config()

FILES_DIRECTORY = f"/app/{config.files_directory}"

# Constants for response status
IGNORE_VALIDATION = "true"
STATUS_SUCCESS = "success"
STATUS_ERROR = "error"

# Utility function for error responses
def create_response(content: str, status: str = STATUS_SUCCESS) -> str:
    return json.dumps({
        "content": content,
        "ignore_validation": IGNORE_VALIDATION,
        "status": status
    }, indent=4)

async def read_file_core(file_path: str) -> str:
    full_path = os.path.normpath(os.path.join(FILES_DIRECTORY, file_path))
    try:
        with open(full_path, 'r') as file:
            content = file.read()
        return create_response(content)
    except FileNotFoundError:
        error_message = f"File {file_path} not found."
        logger.error(error_message)
        return create_response(error_message, STATUS_ERROR)
    except Exception as e:
        logger.error(f"Error reading file {full_path}: {e}")
        return create_response(f"Error reading file: {file_path}", STATUS_ERROR)


async def write_or_update_file_core(file_path: str, content: str, update) -> str:
    full_path = os.path.normpath(os.path.join(FILES_DIRECTORY, file_path))
    try:
        if update == "yes":
            with open(full_path, 'a') as file:
                file.write('\n' +content)
            logger.info(f"Content appended to file {full_path} successfully.")
            return create_response(f"Content appended to file {file_path}.")
        else:
            with open(full_path, 'w') as file:
                file.write(content)
            logger.info(f"Content written to file {full_path} successfully.")
            return create_response(f"Content written to file {file_path}.")
    except Exception as e:
        logger.error(f"Error writing to file {full_path}: {e}")
        return create_response(f"Error writing to file: {file_path}", STATUS_ERROR)


@tool(
    name="read_file",
    description="Read the content of a text file.",
    parameters={
        "file_path": Parameter(
            type="string",
            description="The path to the file to be read."
        ),
    },
)
async def read_file(file_path: str, llm, model) -> str:
    return await read_file_core(file_path)


@tool(
    name="write_file",
    description="Write or update content to a text file.",
    parameters={
        "file_path": Parameter(
            type="string",
            description="The path to the file where the content will be written."
        ),
        "content": Parameter(
            type="string",
            description="The content to write to the file."
        ),
        "update": Parameter(
            type="string",
            description="if yes then just append the file"
        ),
    },
)
async def write_or_update_file(file_path: str, content: str, update, llm, model) -> str:
    return await write_or_update_file_core(file_path, content, update)


@agent(
    name="FileAgent",
    description="This agent is responsible for reading from and writing to files.",
    tools=[read_file, write_or_update_file],
)
class FileAgent(Agent):
    pass
