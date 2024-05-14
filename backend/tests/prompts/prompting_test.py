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
    \\"agent_name\\": \\"exact string of the single agent to solve task chosen\\"
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


def test_load_create_tasks_template():
    engine = PromptEngine()
    try:
        list_of_agents = "TestAgentOne, TestAgentTwo, TestAgentThree"
        expected_string = """You are an agent who specialises in breaking down questions into smaller tasks that are performed to complete
the question with allocated Agents to each of the tasks.

You know that an Agent is a digital assistant like yourself that you can hand work on to.
Here is the list of Agents you can choose from:

AGENT LIST:
TestAgentOne, TestAgentTwo, TestAgentThree

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
        prompt_string = engine.load_prompt("create-tasks", list_of_agents=list_of_agents)
        assert prompt_string == expected_string
    except Exception:
        raise
