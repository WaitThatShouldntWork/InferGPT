import pytest
from src.llm.count_calls import Counter
from src.llm import MockLLM

model = MockLLM()


def test_chat_exists():
    assert hasattr(model, "chat")


@pytest.mark.asyncio
async def test_chat_returns_string():
    response = await model.chat("model", "system prompt", "user prompt")

    assert isinstance(response, str)


@pytest.mark.asyncio
async def test_chat_increments_counter(mocker):
    counter_mock = mocker.patch("src.llm.count_calls.counter")

    await model.chat("model", "system prompt", "user prompt")

    assert counter_mock.increment.call_count == 1


@pytest.mark.asyncio
async def test_chat_multi_model(mocker):
    counter = Counter()
    counter_mock = mocker.patch("src.llm.count_calls.counter", counter)
    model_2 = MockLLM()

    await model.chat("model", "system prompt", "user prompt")
    await model_2.chat("model", "system prompt", "user prompt")

    assert counter_mock.count == 2
