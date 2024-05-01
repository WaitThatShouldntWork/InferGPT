from unittest.mock import MagicMock
from mistralai.models.chat_completion import ChatCompletionResponse
from mistralai.models.chat_completion import ChatCompletionResponseChoice
from mistralai.models.chat_completion import ChatMessage
from mistralai.models.common import UsageInfo
from src.utils import Config, call_model, call_model_with_tools, MistralClient

system_prompt = "system_prompt"
user_prompt = "user_prompt"
content_response = "Hello there"


def create_mock_chat_response(content, tool_calls=None):
    mock_usage = UsageInfo(prompt_tokens=1, total_tokens=2, completion_tokens=3)
    mock_message = ChatMessage(role="system", content=content, tool_calls=tool_calls)
    mock_choice = ChatCompletionResponseChoice(index=0, message=mock_message, finish_reason=None)
    return ChatCompletionResponse(
        id="id", object="object", created=123, model="model", choices=[mock_choice], usage=mock_usage
    )


mock_client = MagicMock(spec=MistralClient)
mock_config = MagicMock(spec=Config)


def test_call_model_content_string_returns_string(mocker):
    client_instance = mocker.patch("src.utils.llm.client", return_value=mock_client)
    client_instance.chat.return_value = create_mock_chat_response(content_response)

    response = call_model(system_prompt, user_prompt)

    assert response == content_response


def test_call_model_content_list_returns_string(mocker):
    content_list = ["Hello", "there"]
    client_instance = mocker.patch("src.utils.llm.client", return_value=mock_client)
    client_instance.chat.return_value = create_mock_chat_response(content_list)

    response = call_model(system_prompt, user_prompt)

    assert response == content_response


def test_call_model_calls_client_chat(mocker):
    config_instance = mocker.patch("src.utils.llm.config", return_value=mock_config)
    client_instance = mocker.patch("src.utils.llm.client", return_value=mock_client)

    call_model(system_prompt, user_prompt)

    expected_messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=user_prompt),
    ]
    client_instance.chat.assert_called_once_with(
        messages=expected_messages, model=config_instance.mistral_model, tool_choice=None, tools=None, temperature=0
    )


tools = [
    {
        "type": "function",
        "function": {
            "description": "mock tool",
            "name": "mock_tool",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "A name.",
                    },
                },
                "required": ["name"],
            },
        },
    }
]

tool_calls = [{"id": "1", "type": "function", "function": {"name": "mock_tool", "arguments": '{ "name": "Bob" }'}}]


def test_call_model_with_tools_returns_tuple(mocker):
    client_instance = mocker.patch("src.utils.llm.client", return_value=mock_client)
    client_instance.chat.return_value = create_mock_chat_response(content_response, tool_calls=tool_calls)

    (name, params) = call_model_with_tools(system_prompt, user_prompt, tools)

    assert name == "mock_tool"
    assert params == {"name": "Bob"}


def test_call_model_with_tools_calls_client_chat(mocker):
    client_instance = mocker.patch("src.utils.llm.client", return_value=mock_client)
    client_instance.chat.return_value = create_mock_chat_response(content_response, tool_calls=tool_calls)
    config_instance = mocker.patch("src.utils.llm.config", return_value=mock_config)

    call_model_with_tools(system_prompt, user_prompt, tools)

    expected_messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=user_prompt),
    ]
    client_instance.chat.assert_called_once_with(
        messages=expected_messages, model=config_instance.mistral_model, tool_choice="any", tools=tools, temperature=0
    )
