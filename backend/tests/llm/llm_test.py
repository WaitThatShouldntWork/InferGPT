from src.llm.count_calls import Counter
from src.llm import MockLLM

model = MockLLM()


def test_chat_exists():
    assert hasattr(model, "chat")


def test_chat_returns_string():
    response = model.chat("system prompt", "user prompt")

    assert isinstance(response, str)


def test_chat_increments_counter(mocker):
    counter_mock = mocker.patch("src.llm.count_calls.counter")

    model.chat("system prompt", "user prompt")

    assert counter_mock.increment.call_count == 1


def test_chat_multi_model(mocker):
    counter = Counter()
    counter_mock = mocker.patch("src.llm.count_calls.counter", counter)
    model_2 = MockLLM()

    model.chat("system prompt", "user prompt")
    model_2.chat("system prompt", "user prompt")

    assert counter_mock.count == 2
