# Data

A directory for all util and service modules for storing, manipulating and retrieving data

InferGPT uses a Neo4j Knowledge Graph exclusively.

# Setup

1. Create .env files. There are template files (.env.example) for you to copy with comments for guidance.
2. If you're running the service locally, set up Neo4j Desktop as guided in the section below.
If you're running the service using Docker, ignore this step.

## Using Neo4j Desktop

This can be downloaded [here](https://neo4j.com/download/)

Once installed follow the steps below:

1. Create new project to host your DBMS.
2. Create a new database within the project.
3. Add the username and password to the `backend/.env` file.
4. Add the database uri to the `backend/.env` file. The default value for this is `bolt://localhost:7687`
5. Run the database in Neo4j desktop.
6. Test the connection is working by asking InferGPT the keyphrase "healthcheck". 
It will return with a status update on the state of the backend and database


# To do

- [x] Create `neo4j_utils` module and connect to a neo4j knowledge graph
- [ ] Create dockerised neo4j graph that can be run here
- [ ] Create cypher script for setting up graph if running the service locally
