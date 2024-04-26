import json
import logging
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatCompletionResponse, ChatMessage
from utils import Config

logger = logging.getLogger(__name__)
config = Config()

client = MistralClient(api_key=config.mistral_key)


def call_model(system_prompt, user_prompt):
    response = get_response(system_prompt, user_prompt)
    return response.choices[0].message.content


def call_model_with_tools(system_prompt, user_prompt, tools):
    response = get_response(system_prompt, user_prompt, tools)
    tool_calls = response.choices[0].message.tool_calls
    if tool_calls is None:
        raise ValueError("No tool calls found in response")
    tool_call = tool_calls[0]
    function_name = tool_call.function.name
    function_params = json.loads(tool_call.function.arguments)
    return (function_name, function_params)


def get_response(system_prompt, user_prompt, tools=None) -> ChatCompletionResponse:
    tool_choice = None if tools is None else "any"

    logger.debug(
        "Called llm. Waiting on response model with prompt {0}. Tool choice: {1}".format(
            str([system_prompt, user_prompt]), tool_choice
        )
    )

    response = client.chat(
        model=config.mistral_model,
        messages=[
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_prompt),
        ],
        tools=tools,
        tool_choice=tool_choice,
        temperature=0
    )
    logger.debug('{0} response : "{1}"'.format(config.mistral_model, response.choices[0].message.content))
    return response


# TODO: Refactor - 1 get_response method and 1 call_model method
def get_response_three_prompts(
        agent_list_prompt,
        response_format_prompt,
        best_next_step_prompt
    ) -> ChatCompletionResponse:

    logger.debug("Called llm. Waiting on response model with prompts{0}".format(
        str([agent_list_prompt, response_format_prompt, best_next_step_prompt])
    ))

    response = client.chat(
        model=config.mistral_model,
        messages=[
            ChatMessage(role="system", content=agent_list_prompt),
            ChatMessage(role="system", content=response_format_prompt),
            ChatMessage(role="user", content=best_next_step_prompt),
        ]
    )
    logger.debug('{0} response : "{1}"'.format(config.mistral_model, response.choices[0].message.content))
    return response.choices[0].message.content
