from src.utils import call_model
from src.utils.graph_db_utils import run_query
import logging
from src.prompts import PromptEngine
import json


logger = logging.getLogger(__name__)

engine = PromptEngine()

finalised_graph_structure = {'nodes':{}, 'properties':{}}

neo4j_graph_why_prompt = engine.load_prompt("neo4j-graph-why")

# relationship query
relationship_query = engine.load_prompt("relationships-query")
# node query
node_query = engine.load_prompt("nodes-query")
# relationship property query
relationship_property_query = engine.load_prompt("relationship-property-cypher-query")
# node property query
node_relationship_query = engine.load_prompt("node-property-cypher-query")

# relationship prompt
neo4j_relationships_understanding_prompt = engine.load_prompt("neo4j-relationship-understanding",
                                                              neo4j_graph_why_prompt=neo4j_graph_why_prompt)
# nodes prompt
neo4j_nodes_understanding_prompt = engine.load_prompt("neo4j-nodes-understanding",
                                                      neo4j_graph_why_prompt=neo4j_graph_why_prompt)
# relationship property prompt
neo4j_relationship_property_prompt = engine.load_prompt("neo4j-property-intent-prompt",
                                                      neo4j_graph_why_prompt=neo4j_graph_why_prompt)
# node property prompt
neo4j_node_property_prompt = engine.load_prompt("neo4j-node-property",
                                                neo4j_graph_why_prompt=neo4j_graph_why_prompt)


def extract_json_from_response(response):
    """Extract JSON content from a response wrapped in ```json``` markers."""
    start_index = response.find("```json")
    if start_index == -1:
        return None
    start_index += 8
    end_index = response.rfind("```")
    if end_index == -1:
        return None
    return response[start_index:end_index]

def enrich_data(prompt, data):
    """Enrich data by calling the model with a prompt."""
    enriched_data = call_model(prompt, str(data))
    enriched_data = extract_json_from_response(enriched_data)
    if enriched_data:
        return json.loads(enriched_data)
    return None

# Fetch and enrich relationships
relationship_result = run_query(relationship_query)
relationships_neo4j = relationship_result[0]
enriched_relationships = enrich_data(neo4j_relationships_understanding_prompt, relationships_neo4j)
finalised_graph_structure['relationships'] = enriched_relationships if enriched_relationships else {}

# Fetch and enrich nodes
nodes_neo4j_result = run_query(node_query)
nodes_neo4j = nodes_neo4j_result[0]
enriched_nodes = enrich_data(neo4j_nodes_understanding_prompt, nodes_neo4j)
finalised_graph_structure['nodes']['labels'] = enriched_nodes['nodes'] if enriched_nodes else []

# Fetch and enrich relationship properties
properties_result = run_query(relationship_property_query)
rel_properties_neo4j = properties_result[0]

cleaned_rel_properties = [
    {**rel_property, 'properties': [prop for prop in rel_property['properties'] if prop['name'] is not None]}
    for rel_property in rel_properties_neo4j['relProperties']
    if any(prop['name'] is not None for prop in rel_property['properties'])
]

enriched_rel_properties = enrich_data(neo4j_relationship_property_prompt, {'relProperties': cleaned_rel_properties})
finalised_graph_structure['properties']['relationship_properties'] = enriched_rel_properties['relProperties'] if enriched_rel_properties else []

# Fetch and enrich node properties
node_properties_neo4j_result = run_query(node_relationship_query)
node_properties_neo4j = node_properties_neo4j_result[0]
enriched_node_properties = enrich_data(neo4j_node_property_prompt, node_properties_neo4j)
finalised_graph_structure['properties']['node_properties'] = enriched_node_properties['nodeProperties'] if enriched_node_properties else []

graph_structure = json.dumps(finalised_graph_structure, separators=(',', ':'))
