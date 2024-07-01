from abc import ABC, ABCMeta, abstractmethod
from .count_calls import count_calls


class LLMMeta(ABCMeta):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if not hasattr(cls, "instances"):
            cls.instances = {}

        cls.instances[name.lower()] = cls()

    def __new__(cls, name, bases, attrs):
        if "chat" in attrs:
            attrs["chat"] = count_calls(attrs["chat"])

        return super().__new__(cls, name, bases, attrs)


class LLM(ABC, metaclass=LLMMeta):
    @classmethod
    def get_instances(cls):
        return cls.instances

    @abstractmethod
    def chat(self, model: str, system_prompt: str, user_prompt: str) -> str:
        pass
