import logging
from typing import cast
from unittest.mock import AsyncMock, MagicMock
from mistralai import UNSET, AssistantMessage, Mistral as MistralApi, SystemMessage, UserMessage
from mistralai.models import ChatCompletionResponse, ChatCompletionChoice, UsageInfo
import pytest
from src.llm import get_llm, Mistral
from src.utils import Config

mock_model = "mockmodel"
system_prompt = "system_prompt"
user_prompt = "user_prompt"
content_response = "Hello there"

mistral = cast(Mistral, get_llm("mistral"))


def create_mock_chat_response(content, tool_calls=None):
    mock_usage = UsageInfo(prompt_tokens=1, total_tokens=2, completion_tokens=3)
    mock_message = AssistantMessage(content=content, tool_calls=tool_calls)
    mock_choice = ChatCompletionChoice(index=0, message=mock_message, finish_reason="stop")
    return ChatCompletionResponse(
        id="id", object="object", created=123, model="model", choices=[mock_choice], usage=mock_usage
    )


mock_client = AsyncMock(spec=MistralApi)
mock_config = MagicMock(spec=Config)


@pytest.mark.asyncio
async def test_chat_content_string_returns_string(mocker):
    mistral.client = mocker.AsyncMock(return_value=mock_client)
    mistral.client.chat.complete_async.return_value = create_mock_chat_response(content_response)

    response = await mistral.chat(mock_model, system_prompt, user_prompt)

    assert response == content_response


@pytest.mark.asyncio
async def test_chat_calls_client_chat(mocker):
    mistral.client = mocker.AsyncMock(return_value=mock_client)

    await mistral.chat(mock_model, system_prompt, user_prompt)

    expected_messages = [
        SystemMessage(content=system_prompt),
        UserMessage(content=user_prompt),
    ]
    mistral.client.chat.complete_async.assert_awaited_once_with(
        messages=expected_messages, model=mock_model, temperature=0, response_format=None
    )


@pytest.mark.asyncio
async def test_chat_response_none_logs_error(mocker, caplog):
    mistral.client = mocker.AsyncMock(return_value=mock_client)
    mistral.client.chat.complete_async.return_value = None

    response = await mistral.chat(mock_model, system_prompt, user_prompt)

    assert response == "An error occurred while processing the request."
    assert (
        "src.llm.mistral",
        logging.ERROR,
        "Call to Mistral API failed: No valid response or choices received",
    ) in caplog.record_tuples


@pytest.mark.asyncio
async def test_chat_response_choices_none_logs_error(mocker, caplog):
    mistral.client = mocker.AsyncMock(return_value=mock_client)
    chat_response = create_mock_chat_response(content_response)
    chat_response.choices = None
    mistral.client.chat.complete_async.return_value = chat_response

    response = await mistral.chat(mock_model, system_prompt, user_prompt)

    assert response == "An error occurred while processing the request."
    assert (
        "src.llm.mistral",
        logging.ERROR,
        "Call to Mistral API failed: No valid response or choices received",
    ) in caplog.record_tuples


@pytest.mark.asyncio
async def test_chat_response_choices_empty_logs_error(mocker, caplog):
    mistral.client = mocker.AsyncMock(return_value=mock_client)
    chat_response = create_mock_chat_response(content_response)
    chat_response.choices = []
    mistral.client.chat.complete_async.return_value = chat_response

    response = await mistral.chat(mock_model, system_prompt, user_prompt)

    assert response == "An error occurred while processing the request."
    assert (
        "src.llm.mistral",
        logging.ERROR,
        "Call to Mistral API failed: No valid response or choices received",
    ) in caplog.record_tuples


@pytest.mark.asyncio
async def test_chat_response_choices_message_content_none_logs_error(mocker, caplog):
    mistral.client = mocker.AsyncMock(return_value=mock_client)
    chat_response = create_mock_chat_response(content_response)
    assert chat_response.choices is not None
    chat_response.choices[0].message.content = None
    mistral.client.chat.complete_async.return_value = chat_response

    response = await mistral.chat(mock_model, system_prompt, user_prompt)

    assert response == "An error occurred while processing the request."
    assert (
        "src.llm.mistral",
        logging.ERROR,
        "Call to Mistral API failed: message content is None or Unset",
    ) in caplog.record_tuples


@pytest.mark.asyncio
async def test_chat_response_choices_message_content_unset_logs_error(mocker, caplog):
    mistral.client = mocker.AsyncMock(return_value=mock_client)
    chat_response = create_mock_chat_response(content_response)
    assert chat_response.choices is not None
    chat_response.choices[0].message.content = UNSET
    mistral.client.chat.complete_async.return_value = chat_response

    response = await mistral.chat(mock_model, system_prompt, user_prompt)

    assert response == "An error occurred while processing the request."
    assert (
        "src.llm.mistral",
        logging.ERROR,
        "Call to Mistral API failed: message content is None or Unset",
    ) in caplog.record_tuples
