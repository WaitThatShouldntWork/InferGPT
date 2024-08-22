# GraphDB Sample

## Cypher

This folder contains a number of CSV files used to build a sample graphdb for the chatbot. Single word filenames (goals, knowledge etc.) are for nodes. Two words separated by an underscore are for relationships (e.g. profiles_knowledge links profile nodes to knowledge nodes) - the naming is left-to-right in the direction of the relationship.

There are three Cypher script files as below. Use clear_graph to create / re-create the DB before using create_graph.

1. clear_graph.cypher - this recreates a blank database (create or replace). This **will** destroy all data in the DB if it already exists. Copy/paste and execute each line.
2. create_graph.cypher - imports all of the CSV files to create a sample graph. The graph has users and possible conversations but does not (currently) include any conversation relationships. Copy/paste and execute the :use statement before copy/pasting all of the subsequent statements together. ** You will need to host the CSV files so that neo4j can access them. If you use the recommended [live server extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) for VS Code, this should 'just work' once you start live server (bottom-right of VS Code status bar to stop/start). **
3. scripts.cypher - a collection of (parameterized) scripts for different queries / updates that will be required to use the graph db in the chatbot.

## Postman

There is an exported Postman collection of requests (chatBot.postman_collection.json). This is only a starting point - the authentication isn't working and hasn't been looked into. To make this work, the authentication needs fixing. The collection requires the following variables:

* username - Username to connect with (probably neo4j)
* password - Password for the user above
* baseUrl - URL to POST the HTTP API requests to
* discoveryUrl - an unauthenticated request that will return the endpoints for the server

** NOTE: Postman is probably not required as the Neo4j Python package should be able to handle all of the Neo4j API interaction for us. **
