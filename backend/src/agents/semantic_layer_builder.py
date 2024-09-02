# NOT NEEDED CURRENTLY AS THE RETURNED VALUE OF GRAPH SCHEMA IS STORED STATICALLY AS A JINJA TEMPLATE
# THIS FILE IS CURRENTLY BROKEN BUT AS UNUSED THE FOLLOWING LINE IS SUPRESSING ERRORS
# REMOVE NEXT LINE BEFORE WORKING ON FILE
# pyright: reportAttributeAccessIssue=none
from src.utils.graph_db_utils import execute_query
import logging
from src.prompts import PromptEngine
import json

logger = logging.getLogger(__name__)

engine = PromptEngine()


async def get_semantic_layer(llm, model):
    finalised_graph_structure = {"nodes": {}, "properties": {}}

    neo4j_graph_why_prompt = engine.load_prompt("neo4j-graph-why")

    relationship_query = engine.load_prompt("relationships-query")

    node_query = engine.load_prompt("nodes-query")

    relationship_property_query = engine.load_prompt("relationship-property-cypher-query")

    node_property_query = engine.load_prompt("node-property-cypher-query")

    neo4j_relationships_understanding_prompt = engine.load_prompt(
        "neo4j-relationship-understanding", neo4j_graph_why_prompt=neo4j_graph_why_prompt
    )

    neo4j_nodes_understanding_prompt = engine.load_prompt(
        "neo4j-nodes-understanding", neo4j_graph_why_prompt=neo4j_graph_why_prompt
    )

    neo4j_relationship_property_prompt = engine.load_prompt(
        "neo4j-property-intent-prompt", neo4j_graph_why_prompt=neo4j_graph_why_prompt
    )

    neo4j_node_property_prompt = engine.load_prompt(
        "neo4j-node-property", neo4j_graph_why_prompt=neo4j_graph_why_prompt
    )

    # Fetch and enrich relationships
    relationship_result = execute_query(relationship_query)
    relationships_neo4j = relationship_result[0]
    enriched_relationships = await llm.chat(model, neo4j_relationships_understanding_prompt, str(relationships_neo4j))
    if enriched_relationships.startswith("```json") and enriched_relationships.endswith("```"):
      enriched_relationships = enriched_relationships[7:-3].strip()
    enriched_relationships = json.dumps(enriched_relationships)
    enriched_relationships = json.loads(enriched_relationships)
    finalised_graph_structure["relationships"] = enriched_relationships if enriched_relationships else {}

    # Fetch and enrich nodes
    nodes_neo4j_result = execute_query(node_query)
    nodes_neo4j = nodes_neo4j_result[0]
    enriched_nodes = await llm.chat(model, neo4j_nodes_understanding_prompt, str(nodes_neo4j))
    if enriched_nodes.startswith("```json") and enriched_nodes.endswith("```"):
      enriched_nodes = enriched_nodes[7:-3].strip()
    enriched_nodes = json.loads(enriched_nodes)
    json.dumps(enriched_nodes)
    finalised_graph_structure['nodes']['labels'] = enriched_nodes['nodes']
    logger.debug(f"Finalised graph structure with enriched nodes: {finalised_graph_structure}")

    # Fetch and enrich node properties
    node_properties_neo4j_result = execute_query(node_property_query)
    node_properties_neo4j = node_properties_neo4j_result[0]
    filtered_payload = {
        'nodeProperties': [
            node for node in node_properties_neo4j['nodeProperties']
            if all(prop['data_type'] is not None and prop['name'] is not None for prop in node['properties'])
        ]
    }
    enriched_node_properties = await llm.chat(model, neo4j_node_property_prompt, str(filtered_payload))
    if enriched_node_properties.startswith("```json") and enriched_node_properties.endswith("```"):
        enriched_node_properties = enriched_node_properties[7:-3].strip()
    enriched_node_properties = json.loads(enriched_node_properties)

    finalised_graph_structure["properties"]["node_properties"] = enriched_node_properties["nodeProperties"]
    logger.debug(f"Finalised graph structure with enriched node properties: {finalised_graph_structure}")
    return finalised_graph_structure
