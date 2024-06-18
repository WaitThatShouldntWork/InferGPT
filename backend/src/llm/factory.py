from .llm import LLM

def get_llm(name: str | None) -> LLM:
    if name is None:
        raise ValueError("LLM name not provided")

    llm = LLM.get_instances().get(name)

    if llm is None:
        raise ValueError(f"No LLM model found for: {name}")

    return llm
