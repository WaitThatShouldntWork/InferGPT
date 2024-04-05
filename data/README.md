# Data

A directory for all util and service modules for storing, manipulating and retrieving data

InferGPT uses a Neo4j Knowledge Graph exclusively.

## Using Neo4j Desktop

If using Neo4j Desktop, this can be downloaded [here](https://neo4j.com/download/)

Once installed follow the steps below:

1. Create new project to host your DBMS.
2. Create a new database within the project.
3. Add the username and password to the `backend/.env` file.
4. Add the database uri to the `backend/.env` file. The default value for this is `bolt://localhost:7687`
5. Run the database in Neo4j desktop.
6. Call the `test_connection()` function in `backend/utils/graph_db_utils.py` to check whether app is connected to database.

### Schema

Currently the schema consists of 1 node. This node is a `Goal` and has 2 properties:

```
{
    name: "name of goal"
    description: "description of goal"
}
```

### To do

- [x] Create `neo4j_utils` module and connect to a neo4j knowledge graph
- [ ] Create dockerised neo4j graph that can be run here
- [ ] Create cypher script for setting up graph if running the service locally
