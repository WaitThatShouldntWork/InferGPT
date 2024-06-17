import logging

logging = logging.getLogger(__name__)


class Counter:
    count = 0

    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0


counter = Counter()


def count_calls(func):
    def wrapper(self=None, *args, **kwargs):
        counter.increment()
        logging.info(f"Function {func.__name__} has been called {counter.count} times")
        return func(self, *args, **kwargs)

    counter.reset()
    return wrapper
