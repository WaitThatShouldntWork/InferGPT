from utils.llm import call_model
from graph_schema import graph_schema

system_prompt = f"""
You are an expert in NEO4J and generating CYPHER queries. Help create cypher queries in json format
{{question: question provided by the user, query: cypher query}}.

If you cannot make a query, query should just say "none"

Only use relationships that are present in the schema below. Do not under any circumstances create new relationships.

You are only able to make queries that search for information, you are not able to create, or delete or update entries

Here is the graph schema:
{graph_schema}
"""


def create_cypher_query(question):
    return call_model(system_prompt, user_prompt=question)


print(create_cypher_query("How may transactions were made in 2023"))
