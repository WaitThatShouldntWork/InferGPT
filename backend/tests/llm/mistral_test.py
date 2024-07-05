from typing import cast
from unittest.mock import MagicMock
from mistralai.models.chat_completion import ChatCompletionResponse
from mistralai.models.chat_completion import ChatCompletionResponseChoice
from mistralai.models.chat_completion import ChatMessage
from mistralai.models.common import UsageInfo
from src.llm import get_llm, MistralClient, Mistral
from src.utils import Config

mock_model = "mockmodel"
system_prompt = "system_prompt"
user_prompt = "user_prompt"
content_response = "Hello there"

mistral = cast(Mistral, get_llm("mistral"))


def create_mock_chat_response(content, tool_calls=None):
    mock_usage = UsageInfo(prompt_tokens=1, total_tokens=2, completion_tokens=3)
    mock_message = ChatMessage(role="system", content=content, tool_calls=tool_calls)
    mock_choice = ChatCompletionResponseChoice(index=0, message=mock_message, finish_reason=None)
    return ChatCompletionResponse(
        id="id", object="object", created=123, model="model", choices=[mock_choice], usage=mock_usage
    )


mock_client = MagicMock(spec=MistralClient)
mock_config = MagicMock(spec=Config)


def test_chat_content_string_returns_string(mocker):
    mistral.client = mocker.MagicMock(return_value=mock_client)
    mistral.client.chat.return_value = create_mock_chat_response(content_response)

    response = mistral.chat(mock_model, system_prompt, user_prompt)

    assert response == content_response


def test_chat_content_list_returns_string(mocker):
    content_list = ["Hello", "there"]
    mistral.client = mocker.MagicMock(return_value=mock_client)
    mistral.client.chat.return_value = create_mock_chat_response(content_list)

    response = mistral.chat(mock_model, system_prompt, user_prompt)

    assert response == content_response


def test_chat_calls_client_chat(mocker):
    mistral.client = mocker.MagicMock(return_value=mock_client)

    mistral.chat(mock_model, system_prompt, user_prompt)

    expected_messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=user_prompt),
    ]
    mistral.client.chat.assert_called_once_with(
        messages=expected_messages, model=mock_model, temperature=0
    )
