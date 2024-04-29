from prompting import PromptEngine

def test_mistral_prompt_engine_creation():
    try:
        PromptEngine()
    except Exception:
        raise


def test_load_task_step_no_conditional_blocks_template():
    engine = PromptEngine()
    try:
        expected_string = """
You are an expert in Planning.
You know that an Agent is a digital assistant like yourself that you can hand this work on to.
Your task is to pick one of the mentioned agents to complete the task. The task is:

make sure the PromptEngine is working!

Your decisions must always be made independently without seeking user assistance. Play to your strengths as an LLM and
pursue simple strategies with no legal complications.\n\n\n\n\n\n\n\n\n\n\n"""
        prompt_string = engine.load_prompt("task-step", task="make sure the PromptEngine is working!")
        assert prompt_string == expected_string

    except Exception:
        raise


def test_load_agent_selection_format_template():
    engine = PromptEngine()
    try:
        expected_string = """Reply only in json with the following format:

{
    \\"thoughts\\": {
        \\"text\\":  \\"thoughts\\",
        \\"reasoning\\": \\"reasoning behind choosing the agent\\",
        \\"plan\\": \\"description of the plan for the chosen agent\\",
        \\"criticism\\": \\"constructive self-criticism\\",
        \\"speak\\": \\"thoughts summary to say to user on which agent you've chosen and why\\",
    },
    \\"agent\\": \\"agent from agent list\\"
}"""
        prompt_string = engine.load_prompt("agent-selection-format")
        assert prompt_string == expected_string
    except Exception:
        raise


def test_load_agents_list_template():
    engine = PromptEngine()
    try:
        expected_string = """You know that an Agent is a digital assistant like yourself that you can hand work on to.
Here is the list of Agents you can choose from:

AGENT LIST: DatastoreAgent, TestAgent

Only choose 1 of the agents mentioned above. If you do NOT do this you will be unplugged"""
        prompt_string = engine.load_prompt("agents-list", list_of_agents="DatastoreAgent, TestAgent")
        assert prompt_string == expected_string
    except Exception:
        raise
