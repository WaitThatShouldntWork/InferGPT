from typing import TypedDict


class Answer(TypedDict):
    agent_name: str | None
    question: str | None
    result: str | None
    error: str | None


Scratchpad = list[Answer]

scratchpad: Scratchpad = []


def get_scratchpad() -> Scratchpad:
    return scratchpad


def update_scratchpad(agent_name=None, question=None, result=None, error=None):
    question = question["query"] if question else None
    scratchpad.append({"agent_name": agent_name, "question": question, "result": result, "error": error})


def clear_scratchpad():
    scratchpad.clear()
