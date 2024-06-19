# NOT NEEDED CURRENTLY AS THE RETURNED VALUE OF GRAPH SCHEMA IS STORED STATICALLY AS A JINJA TEMPLATE

from src.llm import call_model
from src.utils.graph_db_utils import execute_query
import logging
from src.prompts import PromptEngine
import json
import ast

logger = logging.getLogger(__name__)

engine = PromptEngine()

def get_semantic_layer():
    finalised_graph_structure = {'nodes':{}, 'properties':{}}

    neo4j_graph_why_prompt = engine.load_prompt("neo4j-graph-why")

    relationship_query = engine.load_prompt("relationships-query")

    node_query = engine.load_prompt("nodes-query")

    relationship_property_query = engine.load_prompt("relationship-property-cypher-query")

    node_property_query = engine.load_prompt("node-property-cypher-query")

    neo4j_relationships_understanding_prompt = engine.load_prompt("neo4j-relationship-understanding",
                                                                neo4j_graph_why_prompt=neo4j_graph_why_prompt)

    neo4j_nodes_understanding_prompt = engine.load_prompt("neo4j-nodes-understanding",
                                                        neo4j_graph_why_prompt=neo4j_graph_why_prompt)

    neo4j_relationship_property_prompt = engine.load_prompt("neo4j-property-intent-prompt",
                                                        neo4j_graph_why_prompt=neo4j_graph_why_prompt)

    neo4j_node_property_prompt = engine.load_prompt("neo4j-node-property",
                                                    neo4j_graph_why_prompt=neo4j_graph_why_prompt)


    # Fetch and enrich relationships
    relationship_result = execute_query(relationship_query)
    relationships_neo4j = relationship_result[0]
    enriched_relationships = call_model(neo4j_relationships_understanding_prompt, str(relationships_neo4j))
    enriched_relationships = json.dumps(enriched_relationships)
    enriched_relationships = json.loads(enriched_relationships)
    finalised_graph_structure['relationships'] = enriched_relationships if enriched_relationships else {}
    logger.info("Finalised graph structure with enriched relationships: ")
    logger.info(finalised_graph_structure)

    # Fetch and enrich nodes
    nodes_neo4j_result = execute_query(node_query)
    nodes_neo4j = nodes_neo4j_result[0]
    enriched_nodes = call_model(neo4j_nodes_understanding_prompt, str(nodes_neo4j))
    enriched_nodes = ast.literal_eval(enriched_nodes)
    finalised_graph_structure['nodes']['labels'] = enriched_nodes['nodes']
    logger.info("Finalised graph structure with enriched nodes: ")
    logger.info(finalised_graph_structure)

    # Fetch and enrich relationship properties
    properties_result = execute_query(relationship_property_query)
    rel_properties_neo4j = properties_result[0]
    enriched_rel_properties = call_model(neo4j_relationship_property_prompt, str(rel_properties_neo4j))
    enriched_rel_properties = ast.literal_eval(enriched_rel_properties)
    finalised_graph_structure['properties']['relationship_properties'] = enriched_rel_properties['relProperties']
    logger.info("Finalised graph structure with enriched relationship properties: ")
    logger.info(finalised_graph_structure)

    # Fetch and enrich node properties
    node_properties_neo4j_result = execute_query(node_property_query)
    node_properties_neo4j = node_properties_neo4j_result[0]
    enriched_node_properties = call_model(neo4j_node_property_prompt, str(node_properties_neo4j))
    enriched_node_properties = ast.literal_eval(enriched_node_properties)
    finalised_graph_structure['properties']['node_properties'] = enriched_node_properties['nodeProperties']
    logger.info("Finalised graph structure with enriched node properties: ")
    logger.info(finalised_graph_structure)

    graph_schema = json.dumps(finalised_graph_structure, separators=(',', ':'))
    return graph_schema
