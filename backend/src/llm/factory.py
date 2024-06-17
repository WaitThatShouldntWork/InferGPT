from typing import Dict
from .llm import LLM
from .mistral import Mistral


llm_map: Dict[str, LLM] = {"mistral": Mistral()}


def get_llm(type: str | None) -> LLM:
    if type is None:
        raise ValueError("LLM type not provided")

    llm = llm_map.get(type)

    if llm is None:
        raise ValueError(f"No LLM model found for: {type}")

    return llm
