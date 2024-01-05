# from langchain.chains import GraphCypherQAChain
# from langchain.prompts.prompt import PromptTemplate
# from llm import llm
# from graph import graph

# WRITE_CYPHER_GENERATION_TEMPLATE = """
# You are an expert Neo4j Developer translating user information into Cypher to store conversation history and facts gathered about the customer during the conversation.
# Convert the user's information based on the schema.

# Use only the provided relationship types and properties in the schema.
# Do not use any other relationship types or properties that are not provided.

# Fine Tuning:

# For movie titles that begin with "The", move "the" to the end. For example "The 39 Steps" becomes "39 Steps, The" or "the matrix" becomes "Matrix, The".

# Example Cypher Statements:

# 1. How to find how many degrees of separation there are between two people:
# ```
# MATCH path = shortestPath(
#   (p1:Person {{name: "Actor 1"}})-[:ACTED_IN|DIRECTED*]-(p2:Person {{name: "Actor 2"}})
# )
# WITH path, p1, p2, relationships(path) AS rels
# RETURN
#   p1 {{ .name, .born, link:'https://www.themoviedb.org/person/'+ p1.tmdbId }} AS start,
#   p2 {{ .name, .born, link:'https://www.themoviedb.org/person/'+ p2.tmdbId }} AS end,
#   reduce(output = '', i in range(0, length(path)-1) |
#     output + CASE
#       WHEN i = 0 THEN
#        startNode(rels[i]).name + CASE WHEN type(rels[i]) = 'ACTED_IN' THEN ' played '+ rels[i].role +' in 'ELSE ' directed ' END + endNode(rels[i]).title
#        ELSE
#          ' with '+ startNode(rels[i]).name + ', who '+ CASE WHEN type(rels[i]) = 'ACTED_IN' THEN 'played '+ rels[i].role +' in '
#     ELSE 'directed '
#       END + endNode(rels[i]).title
#       END
#   ) AS pathBetweenPeople
# ```

# Schema:
# {schema}

# Question:
# {question}
# """

# cypher_prompt = PromptTemplate.from_template(WRITE_CYPHER_GENERATION_TEMPLATE)

# cypher_qa = GraphCypherQAChain.from_llm(
#     llm,          # (1)
#     graph=graph,  # (2)
#     verbose=True,
#     cypher_prompt=cypher_prompt,
# )