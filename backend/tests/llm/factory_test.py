import pytest
from src.llm.mistral import Mistral
from src.llm import get_llm


def test_get_llm_type_none_throws():
    with pytest.raises(ValueError) as error:
        get_llm(None)

    assert str(error.value) == "LLM type not provided"


def test_get_llm_invalid_type_throws():
    with pytest.raises(ValueError) as error:
        get_llm("invalid")

    assert str(error.value) == "No LLM model found for: invalid"


def test_get_llm_valid_type_returns_llm():
    llm = get_llm("mistral")

    assert isinstance(llm, Mistral)
