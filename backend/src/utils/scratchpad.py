import logging

logger = logging.getLogger(__name__)

scratchpad = []


def get_scratchpad() -> list:
    return scratchpad


def update_scratchpad(agent_name, question, result):
    scratchpad.append({"agent_name": agent_name, "question": question["query"], "result": result})


def clear_scratchpad():
    logger.info("Scratchpad cleared")
    scratchpad.clear()
