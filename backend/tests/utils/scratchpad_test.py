from src.utils.scratchpad import clear_scratchpad, get_scratchpad, update_scratchpad


task = {
    'summary': 'example task', 
    'explanation': 'This is an example task'
}

def test_scratchpad():
    clear_scratchpad()
    assert get_scratchpad() == []
    update_scratchpad("ExampleAgent", task, "example result")
    assert get_scratchpad() == [{'agent_name': 'ExampleAgent', 'task': 'example task', 'result': 'example result'}]
    clear_scratchpad()
