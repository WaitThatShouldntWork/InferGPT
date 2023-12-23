### COACHGPT: your local personalised AI agent

Goal: a local, open source ai agent that uses your data and can infer next best question to provide a personalised experience.

## Context
Language models are great a predicting the next token - as theyre design to. 
The issue though, compared to humans, is when one human makes a request to another, we very rarely just spew out a response.
Instead, we usually ask a question back.
A good example is GPTEngineer: https://github.com/gpt-engineer-org/gpt-engineer

When you first give it a request, it asks "clarifying questions" to ensure its aligned with what you want - but those are generated. 
I want to use a graph to understand the users current profile and ask questions based on missing context needed to solve their issue.
It can then also store conversations, context and new information as times goes on - always remaining contextually updated.

## Why a graph?
Graphs are great at this sort of task. They inference really fast and they carry deep context with their edges.
Most excitingly they also:
1. act as super-vector stores with Neo4j's cypher language, providing better perforfmance vs cosine similiary methods.
2. Make great recommendation models - COACHGPT could even start to predict what you want to do next!

###TODO
(Will migrate this to Issues/projects later)

- Change neo4jvector variable in tools/vector.py to update to new graph
- Get better at CYPHER
- Understand and add a task memory
- Write a txt file summarise results (look to GPTengineer for inspiration)
- Create new graph for financial coach
- Change source of Neo4j graph in secrets.toml
- Add an item

### Running the application

To run the application, you must install the libraries listed in `requirements.txt`.

[source,sh]
pip install -r requirements.txt


Then run the `streamlit run` command to start the app on link:http://localhost:8501/[http://localhost:8501/^].

[source,sh]
streamlit run bot.py

###USAGE 
Coming

LISENCE 
See LISENCE.md