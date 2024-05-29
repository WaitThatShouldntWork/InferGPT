from src.utils import call_model
from src.utils.graph_db_utils import run_query
import logging
from src.prompts import PromptEngine
import json


logger = logging.getLogger(__name__)

current_user = "John Doe"
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



# GET ALL RELATIONSHIPS FROM NEO4J
relationship_result = run_query(relationship_query)
relationships_neo4j = relationship_result[0]

enriched_relationships = call_model(neo4j_relationships_understanding_prompt, str(relationships_neo4j))

# Check if the response is wrapped in ```json ``` markers
if enriched_relationships.startswith("```json") and enriched_relationships.endswith("```"):
    # Remove the code block markers for JSON
    enriched_relationships = enriched_relationships[7:-3].strip()

enriched_relationships = json.loads(enriched_relationships)
finalised_graph_structure['relationships'] = enriched_relationships
print("enriched relationships: " + json.dumps(enriched_relationships, indent=2))



# GET ALL NODES FROM NEO4J
nodes_neo4j_result = run_query(node_query)
nodes_neo4j = nodes_neo4j_result[0]

def call_llm(prompt, neo4j_data):
    enriched_data = call_model(neo4j_relationships_understanding_prompt, str(nodes_neo4j))
    if enriched_data.startswith("```json") and enriched_data.endswith("```"):
        # Remove the code block markers for JSON
        enriched_data = enriched_data[7:-3].strip()

    enriched_data = json.loads(enriched_data)
    if enriched_data.startswith("```json") and enriched_data.endswith("```"):
      # Remove the code block markers for JSON
      enriched_data = enriched_data[7:-3].strip()

    enriched_data = json.loads(enriched_data)

    return enriched_data

enriched_nodes = call_llm(
    prompt = neo4j_relationships_understanding_prompt,
    neo4j_data = nodes_neo4j
)

finalised_graph_structure['nodes']['labels'] = enriched_nodes['nodes']
print("enriched nodes: " + json.dumps(enriched_nodes, indent=2))


# GET ALL RELATIONSHIP PROPERTIES FROM NEO4J
properties_result = run_query(relationship_query)
rel_properties_neo4j = properties_result[0]


# Loop through the payload to remove any properties where "name" = None
cleaned_rel_properties = []
for rel_property in rel_properties_neo4j['relProperties']:
    cleaned_properties = [prop for prop in rel_property['properties'] if prop['name'] is not None]
    if cleaned_properties:  # If there are any properties left after cleaning
        rel_property['properties'] = cleaned_properties
        cleaned_rel_properties.append(rel_property)

rel_properties_neo4j = {'relProperties': cleaned_rel_properties}

enriched_rel_properties = call_model(neo4j_relationship_property_prompt, str(rel_properties_neo4j))
if enriched_rel_properties.startswith("```json") and enriched_rel_properties.endswith("```"):
    # Remove the code block markers for JSON
    enriched_rel_properties = enriched_rel_properties[7:-3].strip()
enriched_rel_properties = json.loads(enriched_rel_properties)
finalised_graph_structure['properties']['relationship_properties'] = enriched_rel_properties['relProperties']
print("enriched properties: " + json.dumps(enriched_rel_properties, indent=2))

# GET ALL NODE RELATIONSHIP PROPERTIES FROM NEO4J
node_properties_neo4j_result = run_query(node_relationship_query)
node_properties_neo4j = node_properties_neo4j_result[0]
# Update details via LLM call
enriched_nodes_properties = call_model(neo4j_node_property_prompt, str(node_properties_neo4j))
# Check if the response is wrapped in ```json ``` markers
if enriched_nodes_properties.startswith("```json") and enriched_nodes_properties.endswith("```"):
    # Remove the code block markers for JSON
    enriched_nodes_properties = enriched_nodes_properties[7:-3].strip()
enriched_node_properties = json.loads(enriched_nodes_properties)

finalised_graph_structure['properties']['node_properties'] = enriched_node_properties['nodeProperties']
print("enriched node properties: " + json.dumps(enriched_node_properties, indent=2))

final_structure = json.dumps(finalised_graph_structure, separators=(',', ':'))
