# import streamlit as st
# from langchain.vectorstores.neo4j_vector import Neo4jVector
# from llm import llm, embeddings
# from langchain.chains import RetrievalQA

# neo4jvector = Neo4jVector.from_existing_index(
#     embeddings,                              # (1)
#     url=st.secrets["NEO4J_URI"],             # (2)
#     username=st.secrets["NEO4J_USERNAME"],   # (3)
#     password=st.secrets["NEO4J_PASSWORD"],   # (4)
#     index_name="moviePlots",                 # (5)
#     node_label="Movie",                      # (6)
#     text_node_property="plot",               # (7)
#     embedding_node_property="plotEmbedding", # (8)
#     retrieval_query="""
# RETURN
#     node.plot AS text,
#     score,
#     {
#         title: node.title,
#         directors: [ (person)-[:DIRECTED]->(node) | person.name ],
#         actors: [ (person)-[r:ACTED_IN]->(node) | [person.name, r.role] ],
#         tmdbId: node.tmdbId,
#         source: 'https://www.themoviedb.org/movie/'+ node.tmdbId
#     } AS metadata
# """
# )

# retriever = neo4jvector.as_retriever()

# kg_qa = RetrievalQA.from_chain_type(
#     llm,                  # (1)
#     chain_type="stuff",   # (2)
#     retriever=retriever,  # (3)
# )