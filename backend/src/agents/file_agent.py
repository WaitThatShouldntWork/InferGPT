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


async def read_file_core(file_path: str) -> str:
    full_path = ""
    try:
        full_path = os.path.normpath(os.path.join(FILES_DIRECTORY, file_path))
        with open(full_path, 'r') as file:
            content = file.read()
        response = {
            "content": content,
            "ignore_validation": "true"
        }
        return json.dumps(response, indent=4)
    except FileNotFoundError:
        error_message = f"File {file_path} not found."
        logger.error(error_message)
        response = {
            "content": error_message,
            "ignore_validation": "error",
        }
        return json.dumps(response, indent=4)
    except Exception as e:
        logger.error(f"Error reading file {full_path}: {e}")
        return json.dumps({"status": "error", "message": f"Error reading file: {e}"})


async def write_file_core(file_path: str, content: str) -> str:
    full_path = ""
    try:
        full_path = os.path.normpath(os.path.join(FILES_DIRECTORY, file_path))
        with open(full_path, 'w') as file:
            file.write(content)
        logger.info(f"Content written to file {full_path} successfully.")
        response = {
            "content": f"Content written to file {file_path}.",
            "ignore_validation": "true",
        }
        return json.dumps(response, indent=4)
    except Exception as e:
        logger.error(f"Error writing to file {full_path}: {e}")
        return json.dumps({"status": "error", "message": f"Error writing to file: {e}"})


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
    description="Write content to a text file.",
    parameters={
        "file_path": Parameter(
            type="string",
            description="The path to the file where the content will be written."
        ),
        "content": Parameter(
            type="string",
            description="The content to write to the file."
        ),
    },
)
async def write_file(file_path: str, content: str, llm, model) -> str:
    return await write_file_core(file_path, content)


@agent(
    name="FileAgent",
    description="This agent is responsible for reading from and writing to files.",
    tools=[read_file, write_file],
)
class FileAgent(Agent):
    pass
