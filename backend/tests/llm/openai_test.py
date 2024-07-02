from typing import cast
from unittest.mock import MagicMock
from openai import OpenAI
from src.llm import get_llm, OpenAI as OpenAIModel
from src.utils import Config
config = Config()

system_prompt = "system_prompt"
user_prompt = "user_prompt"
content_response = "Hello there"
openapi_reponse = "Hello! How can I assist you today?"

openai_model = cast(OpenAIModel, get_llm("openai"))

def create_mock_chat_response(content):
    return {
        "choices": [
            {
                "message": {
                    "role": "system",
                    "content": content
                }
            }
        ]
    }

client = OpenAI(api_key=config.openai_key)

mock_client = MagicMock(spec=client)
mock_config = MagicMock(spec=Config)
mock_config.openai_model = "my_openai_model"

def test_chat_content_string_returns_string(mocker):
    mocker.patch("openai.Completion.create", return_value=create_mock_chat_response(content_response))
    response = openai_model.chat(system_prompt, user_prompt)
    assert response == openapi_reponse

def test_chat_content_list_returns_string(mocker):
    content_list = ["Hello", "there"]
    mocker.patch("openai.Completion.create", return_value=create_mock_chat_response(content_list))
    response = openai_model.chat(system_prompt, user_prompt)
    assert response == openapi_reponse

def test_chat_handles_exception(mocker):
    mocker.patch("src.llm.openai.config", return_value=mock_config)

    response = openai_model.chat(system_prompt, user_prompt)
    assert response == "An error occurred while processing the request."
