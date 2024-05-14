import logging
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatCompletionResponse, ChatMessage
from src.utils import Config

logger = logging.getLogger(__name__)
config = Config()

client = MistralClient(api_key=config.mistral_key)


def get_response_content(response: ChatCompletionResponse) -> str:
    content = response.choices[0].message.content
    return content if isinstance(content, str) else " ".join(content)


def call_model(system_prompt, user_prompt) -> str:
    response = get_response(system_prompt, user_prompt)
    return get_response_content(response)


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
        temperature=0,
    )
    logger.debug('{0} response : "{1}"'.format(config.mistral_model, response.choices[0].message.content))
    return response


# TODO: Refactor - 1 get_response method and 1 call_model method
def get_response_three_prompts(agent_list_prompt, response_format_prompt, best_next_step_prompt) -> str:
    logger.debug(
        "Called llm. Waiting on response model with prompts{0}".format(
            str([agent_list_prompt, response_format_prompt, best_next_step_prompt])
        )
    )

    response = client.chat(
        model=config.mistral_model,
        messages=[
            ChatMessage(role="system", content=agent_list_prompt),
            ChatMessage(role="system", content=response_format_prompt),
            ChatMessage(role="user", content=best_next_step_prompt),
        ],
    )
    logger.debug('{0} response : "{1}"'.format(config.mistral_model, response.choices[0].message.content))

    return get_response_content(response)
