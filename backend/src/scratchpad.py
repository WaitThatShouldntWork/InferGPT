scratchpad = []

def get_scratchpad() -> list:
    return scratchpad

def update_scratchpad(agent_name, task, result):
    scratchpad.append({"agent_name": agent_name, "task": task["summary"], "result": result})
