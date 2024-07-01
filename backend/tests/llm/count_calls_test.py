from src.llm.count_calls import Counter, count_calls


def test_counter_initial_count():
    counter = Counter()

    assert counter.count == 0


def test_counter_increment():
    counter = Counter()

    counter.increment()

    assert counter.count == 1


def test_counter_reset():
    counter = Counter()
    counter.increment()

    counter.reset()

    assert counter.count == 0


def test_counter_increment_multiple():
    counter = Counter()

    counter.increment()
    counter.increment()

    assert counter.count == 2


def test_count_calls(mocker):
    mock_func = mocker.Mock(spec=lambda: None)
    mock_counter = mocker.Mock()
    mocker.patch("src.llm.count_calls.counter", mock_counter)
    wrapped = count_calls(mock_func)

    wrapped()

    mock_func.assert_called_once()
    mock_counter.increment.assert_called_once()
