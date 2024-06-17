from src.llm import LLM


class MockLLM(LLM):
    def chat(self, system_prompt: str, user_prompt: str) -> str:
        return "mocked response"