from prompting import PromptEngine

def test_mistral_prompt_engine_creation():
    try:
        PromptEngine("mistral")
    except Exception:
        raise

def test_load_task_step_template():
    engine = PromptEngine("mistral")
    try:
        engine.load_prompt("task-step")
    except Exception:
        raise

def test_load_agent_selection_format_template():
    engine = PromptEngine("mistral")
    try:
        engine.load_prompt("agent-selection-format")
    except Exception:
        raise
