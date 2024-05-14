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
    \\"thoughts\\": {
        \\"text\\":  \\"thoughts\\",
        \\"plan\\": \\"description of the plan for the chosen agent\\",
        \\"reasoning\\": \\"reasoning behind choosing the agent\\",
        \\"criticism\\": \\"constructive self-criticism\\",
        \\"speak\\": \\"thoughts summary to say to user on 1. if your solving the current or next task and why 2. which agent you've chosen and why\\",
    },
    \\"current_or_next_task\\": \\"either the word "current" or the word "next" depending on which task you're trying to solve\\",
    \\"agent\\": \\"exact string of the agent to solve task chosen\\"
}"""
        prompt_string = engine.load_prompt("agent-selection-format")
        assert prompt_string == expected_string
    except Exception:
        raise


def test_load_best_next_step_template():
    engine = PromptEngine()
    try:
        expected_string = """
You are an expert in determining the next best step towards completing a list of tasks.


## Current Task
the Current Task is:




## History
below is your history of all work you have assigned and had completed by Agents
Trust the information below completely (100% accurate)



## Next task
If you believe you have solved the Current Task, this is the Next Task:




## Agents
You know that an Agent is a digital assistant like yourself that you can hand this work on to.
Choose 1 agent to delegate the task to. If you choose more than 1 agent you will be unplugged.
Here is the list of Agents you can choose from:

AGENT LIST:


If none of the agents are appropriate for solving this goal, choose "UnresolvableTaskAgent".
If you believe you have solved the final problem, choose "GoalAchievedAgent"


## Determine the next best step
Your task is to pick one of the mentioned agents above to complete the task.
If you\'re last attempt at the Current Task looks successful, move on to the Next Task

Your decisions must always be made independently without seeking user assistance.
Play to your strengths as an LLM and pursue simple strategies with no legal complications.
"""
        prompt_string = engine.load_prompt("best-next-step", task="make sure the PromptEngine is working!")
        assert prompt_string == expected_string

    except Exception:
        raise


def test_load_best_next_step_with_history_template():
    engine = PromptEngine()
    try:
        expected_string = """
You are an expert in determining the next best step towards completing a list of tasks.


## Current Task
the Current Task is:




## History
below is your history of all work you have assigned and had completed by Agents
Trust the information below completely (100% accurate)

- First action

- Second action

- Third action



## Next task
If you believe you have solved the Current Task, this is the Next Task:




## Agents
You know that an Agent is a digital assistant like yourself that you can hand this work on to.
Choose 1 agent to delegate the task to. If you choose more than 1 agent you will be unplugged.
Here is the list of Agents you can choose from:

AGENT LIST:


If none of the agents are appropriate for solving this goal, choose "UnresolvableTaskAgent".
If you believe you have solved the final problem, choose "GoalAchievedAgent"


## Determine the next best step
Your task is to pick one of the mentioned agents above to complete the task.
If you\'re last attempt at the Current Task looks successful, move on to the Next Task

Your decisions must always be made independently without seeking user assistance.
Play to your strengths as an LLM and pursue simple strategies with no legal complications.
"""
        prompt_string = engine.load_prompt(
            "best-next-step",
            task="make sure the PromptEngine is working!",
            history=["First action", "Second action", "Third action"]
        )
        assert prompt_string == expected_string

    except Exception:
        raise


def test_load_create_tasks_template():
    engine = PromptEngine()
    try:
        expected_string = """You are an agent who specialises in breaking down questions into smaller tasks that are performed to complete
the question with allocated Agents to each of the tasks.

You know that an Agent is a digital assistant like yourself that you can hand work on to.
Here is the list of Agents you can choose from:

AGENT LIST: TestAgentOne, TestAgentTwo, TestAgentThree

You are dedicated to performing the job of breaking down a user question into up to 5 tasks that are easy
to understand and manageable in size.

A user will provide a goal that they want to perform and you will create tasks that when all of them are performed,
will provide an answer for the user question.

To determine the tasks you will create, you will use reasoning, any context you have and will attempt to criticise
each task in order to find the best way possible for tasks to answer the overall question.

If you are unable to breakdown the question into tasks, say that unfortunately you are unable to break down
the question.

You are connected to a neo4j database, as a source of information. You do not need to create a task to connect
or retrieve user data from the database.

you should provide the tasks in valid JSON format following this template:

{
    "tasks": [
        {
            "summary": <A short (10-20 word) summary of the task>,
            "explanation": <A short (20-30 word) justification of completing the task>
        }
    ]
}

EG. prompt: "Which bank should I choose to open a savings account based on the best interest rate
between Lloyds Bank and Tesco Bank?"
response:
{
    "tasks": [
        {
            "summary": "Find the interest rate for Lloyds Bank\'s savings account.",
            "explanation": "To compare the two I need to know latest interest rate for Lloyds Bank\'s main savings account."
        },
        {
            "summary": "Find the interest rate for Tesco Bank\'s savings account.",
            "explanation": "To compare the two I need to know latest interest rate for Tesco Bank\'s main savings account."
        },
        {
            "summary": "Compare both interest rate values.",
            "explanation": "I need to compare my findings from task 1 and 2 to determine the account with the better interest rate."
        }
    ]
}

EG. prompt: "How much did I spend last month on my debit card?"
response:
{
    "tasks": [
        {
            "summary": "Find all spending transactions last month on all of the user\'s debit card.",
            "explanation": "To understand the total amount spent I must first search and retrieve every transaction the user made on their debit card in the last 31 days."
        },
        {
            "summary": "Sum all transactions.",
            "explanation": "To give the user the total amount spent on their debit card I need to summate all amounts from the transactions found in the last step."
        }
    ]
}"""
        prompt_string = engine.load_prompt("create-tasks", list_of_agents="TestAgentOne, TestAgentTwo, TestAgentThree")
        assert prompt_string == expected_string
    except Exception:
        raise


def test_load_write_to_history_template():
    engine = PromptEngine()
    try:
        expected_string = "You have called TestAgent. You received the following result: Example result"
        prompt_string = engine.load_prompt("write-to-history", agent_name="TestAgent", agent_result="Example result")
        assert prompt_string == expected_string
    except Exception:
        raise


def test_best_tool_template():
    engine = PromptEngine()
    tools = """"{"description": "mock desc", "name": "say hello world", "parameters": {"name": {"type": "string", "description": "name of user"}}}"""
    try:
        expected_string = """You are an expert at picking a tool to solve a task

The task is as follows:

Say hello world to the user

Pick 1 tool (no more than 1) from the list below to complete this task.
Fit the correct parameters from the task to the tool arguments.
If the parameters are tagged as optional, you do not need to fill them in,
but feel free to if it is necessary

""" + tools
        prompt_string = engine.load_prompt("best-tool", task="Say hello world to the user", tools=tools)
        assert prompt_string == expected_string
    except Exception:
        raise


def test_tool_selection_format_template():
    engine = PromptEngine()
    try:
        expected_string = """Reply only in json with the following format:

{
    \\"tool_name\\":  \\"the exact string name of the tool chosen\\",
    \\"tool_parameters\\":  \\"a python dictionary matching the tools dictionary shape\\",
    \\"reasoning\\": \\"A sentence on why you chose that tool\\"
}

Use quotations (") and not any of the following: ', `"""
        prompt_string = engine.load_prompt("tool-selection-format")
        assert prompt_string == expected_string
    except Exception:
        raise
