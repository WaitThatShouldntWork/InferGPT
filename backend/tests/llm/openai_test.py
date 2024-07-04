# tests/test_openai_llm.py
import pytest
from unittest.mock import MagicMock, patch
from src.llm.openai_client import OpenAIClient
from src.utils import Config

mock_config = MagicMock(spec=Config)
mock_config.openai_model = "gpt-3.5-turbo"
system_prompt = "system_prompt"
user_prompt = "user_prompt"
content_response = "Hello there"
openapi_response = "Hello! How can I assist you today?"

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

@patch("src.llm.openai_client.openai.ChatCompletion.create")
def test_chat_content_string_returns_string(mock_create):
    mock_create.return_value = create_mock_chat_response(content_response)
    client = OpenAIClient(api_key='fake-api-key')
    response = client.chat(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],)
    assert response == content_response

@patch("src.llm.openai_client.openai.ChatCompletion.create")
def test_chat_content_list_returns_string(mock_create):
    content_list = ["Hello", "there"]
    mock_create.return_value = create_mock_chat_response(content_list)

    client = OpenAIClient(api_key='fake-api-key')
    response = client.chat(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    assert " ".join(response) == content_response

@patch("src.llm.openai_client.openai.ChatCompletion.create")
def test_chat_handles_exception(mock_create):
    mock_create.side_effect = Exception("API error")

    client = OpenAIClient(api_key='fake-api-key')
    response = client.chat(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    assert response == "An error occurred while processing the request."

if __name__ == "__main__":
    pytest.main()
