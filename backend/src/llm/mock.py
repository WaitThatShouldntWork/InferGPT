from .llm import LLM


class MockLLM(LLM):
    def chat(self, model: str, system_prompt: str, user_prompt: str) -> str:
        return "mocked response"
