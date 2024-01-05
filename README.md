# InferGPT: your local personalised AI agent

Goal: a local, open source ai agent that uses your data and can infer next best question to provide a personalised experience.

### Context
Language models are great a predicting the next token - as theyre design to. 
The issue though, compared to humans, is when one human makes a request to another, we very rarely just spew out a response.
Instead, we usually ask a question back.
A good example is GPTEngineer: https://github.com/gpt-engineer-org/gpt-engineer

When you first give it a request, it asks "clarifying questions" to ensure its aligned with what you want - but those are generated. 
I want to use a graph to understand the users current profile and ask questions based on missing context needed to solve their issue.
It can then also store conversations, context and new information as times goes on - always remaining contextually updated.

### Why a graph?
Graphs are great at this sort of task. They inference really fast and they carry deep context with their edges.
Most excitingly they also:
1. act as super-vector stores with Neo4j's cypher language, providing better perforfmance vs cosine similiary methods.
2. Make great recommendation models - graphs could even start to predict what you want to do next!

# Getting Started

In the top-right corner of the page, click Fork.
Create Fork UI

On the next page, select your GitHub account to create the fork under.
Wait for the forking process to complete. You now have a copy of the repository in your GitHub account.
Clone the Repository To clone the repository, you need to have Git installed on your system. 

Once you have Git installed, follow these steps:

Open your terminal.
Navigate to the directory where you want to clone the repository.
Run the git clone command for the fork you just created

## Clone the Repository

Then open your project in your ide
To run the application, you must install the libraries listed in `requirements.txt`.

pip install -r requirements.txt

## Install Neo4j Desktop or Aura DB
Instructions can be found[here](https://neo4j.com/docs/?utm_medium=PaidSearch&utm_source=google&utm_campaign=GDB&utm_content=EMEA-X-Conversion-GDB-Text&utm_term=neo4j&gclid=Cj0KCQiA1rSsBhDHARIsANB4EJY8wQONKSyNCofQBGAcOGWwNpNh4Z0yj7oGxok8vs2CipPJMjGPcpkaAuw1EALw_wcB)


## Run it
Run your virtual enbiroment and then run the `streamlit run` command to start the app on link:http://localhost:8501/[http://localhost:8501/^].

streamlit run bot.py

### USAGE 
Coming

### LISENCE 
See [LISENCE.md](LISENCE.md)

