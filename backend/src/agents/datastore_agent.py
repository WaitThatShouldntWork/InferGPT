import logging
from src.utils import call_model
from src.utils.graph_db_utils import execute_query
from src.prompts import PromptEngine
from datetime import datetime
from src.utils import to_json
from .types import Parameter
from .agent import Agent, agent
from .tool import tool
from src.utils.graph_db_utils import execute_query, run_query
from src.agents import Agent, agent, tool, Parameter
import logging
from src.prompts import PromptEngine
from datetime import datetime
from src.utils import to_json
import json


logger = logging.getLogger(__name__)

current_user = "John Doe"
engine = PromptEngine()

neo4j_graph_why_prompt = engine.load_prompt("neo4j-graph-why")

cypher_query = engine.load_prompt("relationships-query")
node_relationship_query = engine.load_prompt("node-property-cypher-query")
relationship_query = engine.load_prompt("relationships-query")
node_query = engine.load_prompt("nodes-query")


neo4j_relationships_understanding_prompt = engine.load_prompt("neo4j-relationship-understanding",
                                                              neo4j_graph_why_prompt=neo4j_graph_why_prompt)

neo4j_nodes_understanding_prompt = engine.load_prompt("neo4j-nodes-understanding",
                                                      neo4j_graph_why_prompt=neo4j_graph_why_prompt)

neo4j_relationship_property_prompt = engine.load_prompt("neo4j-property-intent-prompt",
                                                      neo4j_graph_why_prompt=neo4j_graph_why_prompt)

neo4j_node_property_prompt = engine.load_prompt("neo4j-node-property",
                                                neo4j_graph_why_prompt=neo4j_graph_why_prompt)
graph_schema_prompt = engine.load_prompt("graph-schema")

generate_cypher_query_prompt = engine.load_prompt(
    "generate-cypher-query", graph_schema_prompt=graph_schema_prompt, current_date=datetime.now()
)


finalised_graph_structure = {'nodes':{}, 'properties':{}}

# GET ALL RELATIONSHIPS FROM NEO4J
result = run_query(cypher_query)
relationships_neo4j = result[0]

enriched_relationships = call_model(neo4j_relationships_understanding_prompt, relationships_neo4j)

# Check if the response is wrapped in ```json ``` markers
if enriched_relationships.startswith("```json") and enriched_relationships.endswith("```"):
    # Remove the code block markers for JSON
    enriched_relationships = enriched_relationships[7:-3].strip()

enriched_relationships = json.loads(enriched_relationships)
finalised_graph_structure['relationships'] = enriched_relationships
print("enriched relationships: " + json.dumps(enriched_relationships, indent=2))



# GET ALL NODES FROM NEO4J
nodes_neo4j = run_query(node_query)
enriched_nodes = call_model(neo4j_nodes_understanding_prompt, nodes_neo4j)
# finalised_graph_structure['nodes']['labels'] = enriched_nodes['nodes']
print("enriched nodes: " + json.dumps(enriched_nodes, indent=2))

# GET ALL RELATIONSHIP PROPERTIES FROM NEO4J
properties_result = run_query(relationship_query)
enriched_rel_properties = call_model(neo4j_relationship_property_prompt, properties_result)
enriched_rel_properties = json.loads(enriched_rel_properties)
finalised_graph_structure['properties']['relationship_properties'] = enriched_rel_properties['relProperties']
print("enriched properties: " + json.dumps(enriched_rel_properties, indent=2))

# GET ALL NODE RELATIONSHIP PROPERTIES FROM NEO4J
node_properties_neo4j = run_query(node_relationship_query)
# Update details via LLM call
enriched_nodes_properties = call_model(neo4j_node_property_prompt, node_properties_neo4j)
# Check if the response is wrapped in ```json ``` markers
if enriched_nodes_properties.startswith("```json") and enriched_nodes_properties.endswith("```"):
    # Remove the code block markers for JSON
    enriched_nodes_properties = enriched_nodes_properties[7:-3].strip()
enriched_node_properties = json.loads(enriched_nodes_properties)
finalised_graph_structure['properties']['node_properties'] = enriched_node_properties['nodeProperties']
print("enriched node properties: " + json.dumps(enriched_node_properties, indent=2))

json.dumps(finalised_graph_structure, separators=(',', ':'))



@tool(
    name="generate cypher query",
    description="Generate Cypher query if the category is data driven, based on the operation to be performed",
    parameters={
        "question_intent": Parameter(
            type="string",
            description="The intent the question will be based on",
        ),
        "operation": Parameter(
            type="string",
            description="The operation the cypher query will have to perform",
        ),
        "question_params": Parameter(
            type="string",
            description="""
                The specific parameters required for the question to be answered with the question_intent
                or none if no params required
            """,
        ),
        "aggregation": Parameter(
            type="string",
            description="Any aggregation that is required to answer the question or none if no aggregation is needed",
        ),
        "sort_order": Parameter(
            type="string",
            description="The order a list should be sorted in or none if no sort_order is needed",
        ),
        "timeframe": Parameter(
            type="string",
            description="string of the timeframe to be considered or none if no timeframe is needed",
        ),
    },
)
def generate_query(question_intent, operation, question_params, aggregation, sort_order, timeframe) -> str:
    details_to_create_cypher_query = engine.load_prompt(
        "details-to-create-cypher-query",
        question_intent=question_intent,
        operation=operation,
        question_params=question_params,
        aggregation=aggregation,
        sort_order=sort_order,
        timeframe=timeframe,
    )
    llm_query = call_model(generate_cypher_query_prompt, details_to_create_cypher_query)
    json_query = to_json(llm_query)
    logger.info("Cypher generated by the LLM: ")
    logger.info(llm_query)
    if json_query["query"] == "None":
        return "No database query"
    db_response = execute_query(json_query["query"])
    logger.info(db_response)
    return str(db_response)


@agent(
    name="DatastoreAgent",
    description="This agent is responsible for handling database queries.",
    tools=[generate_query],
)
class DatastoreAgent(Agent):
    pass
