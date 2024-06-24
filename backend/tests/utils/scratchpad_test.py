from src.utils.scratchpad import clear_scratchpad, get_scratchpad, update_scratchpad


question = {
    "query": "example question",
    "question_intent": "example intent",
    "operation": "example operation",
    "question_category": "example category",
    "parameters": [{"type": "example type", "value": "example value"}],
    "aggregation": "none",
    "sort_order": "none",
    "timeframe": "none",
}


def test_scratchpad():
    clear_scratchpad()
    assert get_scratchpad() == []
    update_scratchpad("ExampleAgent", question, "example result")
    assert get_scratchpad() == [
        {"agent_name": "ExampleAgent", "question": "example question", "result": "example result", "error": None}
    ]
    clear_scratchpad()
