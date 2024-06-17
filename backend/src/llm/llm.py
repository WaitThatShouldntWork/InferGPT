from abc import ABC, ABCMeta, abstractmethod
from .count_calls import count_calls


class LLMMeta(ABCMeta):
    def __new__(cls, name, bases, attrs):
        if "chat" in attrs:
            attrs["chat"] = count_calls(attrs["chat"])

        return super().__new__(cls, name, bases, attrs)


class LLM(ABC, metaclass=LLMMeta):
    @abstractmethod
    def chat(self, system_prompt: str, user_prompt: str) -> str:
        pass
