from src.prompts import PromptEngine


# ruff: noqa: E501
def test_mistral_prompt_engine_creation():
    try:
        PromptEngine()
    except Exception:
        raise


def test_load_agent_selection_format_template():
    engine = PromptEngine()
    try:
        expected_string = """Reply only in json with the following format:

{
    \"thoughts\": {
        \"text\":  \"thoughts\",
        \"plan\": \"description of the plan for the chosen agent\",
        \"reasoning\": \"reasoning behind choosing the agent\",
        \"criticism\": \"constructive self-criticism\",
        \"speak\": \"thoughts summary to say to user on 1. if your solving the current or next task and why 2. which agent you've chosen and why\",
    },
    \"agent_name\": \"exact string of the single agent to solve task chosen\"
}"""
        prompt_string = engine.load_prompt("agent-selection-format")
        assert prompt_string == expected_string
    except Exception:
        raise


def test_load_best_next_step_template():
    engine = PromptEngine()
    try:
        task = "make sure the PromptEngine is working!"
        expected_string = f"""
You are an expert in determining the next best step towards completing a list of tasks.


## Current Task
the Current Task is:

{task}


## History
below is your history of all work you have assigned and had completed by Agents
Trust the information below completely (100% accurate)



## Agents
You know that an Agent is a digital assistant like yourself that you can hand this work on to.
Choose 1 agent to delegate the task to. If you choose more than 1 agent you will be unplugged.
Here is the list of Agents you can choose from:

AGENT LIST:


If the list of agents does not contain something suitable, you should say the agent is 'none'. ie. If question is 'general knowledge', 'personal' or a 'greeting'.

## Determine the next best step
Your task is to pick one of the mentioned agents above to complete the task.
If the same agent_name and task are repeated more than twice in the history, you must not pick that agent_name.

Your decisions must always be made independently without seeking user assistance.
Play to your strengths as an LLM and pursue simple strategies with no legal complications.
"""
        prompt_string = engine.load_prompt("best-next-step", task=task)
        assert prompt_string == expected_string

    except Exception:
        raise


def test_load_best_next_step_with_history_template():
    engine = PromptEngine()
    try:
        task = "make sure the PromptEngine is working!"
        history = ["First action", "Second action", "Third action"]
        expected_string = f"""
You are an expert in determining the next best step towards completing a list of tasks.


## Current Task
the Current Task is:

{task}


## History
below is your history of all work you have assigned and had completed by Agents
Trust the information below completely (100% accurate)
{history}


## Agents
You know that an Agent is a digital assistant like yourself that you can hand this work on to.
Choose 1 agent to delegate the task to. If you choose more than 1 agent you will be unplugged.
Here is the list of Agents you can choose from:

AGENT LIST:


If the list of agents does not contain something suitable, you should say the agent is 'none'. ie. If question is 'general knowledge', 'personal' or a 'greeting'.

## Determine the next best step
Your task is to pick one of the mentioned agents above to complete the task.
If the same agent_name and task are repeated more than twice in the history, you must not pick that agent_name.

Your decisions must always be made independently without seeking user assistance.
Play to your strengths as an LLM and pursue simple strategies with no legal complications.
"""
        prompt_string = engine.load_prompt("best-next-step", task=task, history=history)
        assert prompt_string == expected_string

    except Exception:
        raise


def test_best_tool_template():
    engine = PromptEngine()
    tools = """{\"description\": \"mock desc\", \"name\": \"say hello world\", \"parameters\": {\"name\": {\"type\": \"string\", \"description\": \"name of user\"}}}"""
    try:
        expected_string = """You are an expert at picking a tool to solve a task

The task is as follows:

Say hello world to the user

below is your history of all work you have assigned and had completed by Agents
Trust the information below completely (100% accurate)

scratchpad of history

Pick 1 tool (no more than 1) from the list below to complete this task.
Fit the correct parameters from the task to the tool arguments.
Parameters with required as False do not need to be fit.
Add if appropriate, but do not hallucinate arguments for these parameters

{"description": "mock desc", "name": "say hello world", "parameters": {"name": {"type": "string", "description": "name of user"}}}

From the task you should be able to extract the parameters. If it is data driven, it should be turned into a cypher query

If none of the tools are appropriate for the task, return the following tool

{
    \"tool_name\":  \"None\",
    \"tool_parameters\":  \"{}\",
    \"reasoning\": \"No tool was appropriate for the task\"
}"""
        prompt_string = engine.load_prompt(
            "best-tool", task="Say hello world to the user", scratchpad="scratchpad of history", tools=tools
        )
        assert prompt_string == expected_string
    except Exception:
        raise


def test_tool_selection_format_template():
    engine = PromptEngine()
    try:
        expected_string = """Reply only in json with the following format:

{
    \"tool_name\":  \"the exact string name of the tool chosen\",
    \"tool_parameters\":  \"a JSON object matching the chosen tools dictionary shape\",
    \"reasoning\": \"A sentence on why you chose that tool\"
}"""
        prompt_string = engine.load_prompt("tool-selection-format")
        assert prompt_string == expected_string
    except Exception:
        raise


def test_create_answer_prompt():
    engine = PromptEngine()
    try:
        final_scratchpad = "example scratchpad"
        datetime = "example datetime"
        expected_string = f"""You have been provided the final scratchpad which contains the results for the question in the user prompt.
Your goal is to turn the results into a natural language format to present to the user.

By using the final scratchpad below:
{ final_scratchpad }

and the question in the user prompt, this should be a readable sentence or 2 that summarises the findings in the results.

If the question is a general knowledge question, check if you have the correct details for the answer and reply with this.
If you do not have the answer or you require the internet, do not make it up. You should recommend the user to look this up themselves.
If it is just conversational chitchat. Please reply kindly and direct them to the sort of answers you are able to respond.

The current date and time is { datetime}"""
        prompt_string = engine.load_prompt("create-answer", final_scratchpad=final_scratchpad, datetime=datetime)
        assert prompt_string == expected_string
    except Exception:
        raise
