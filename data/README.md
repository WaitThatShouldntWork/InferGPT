# Data

A directory for all util and service modules for storing, manipulating and retrieving data

InferGPT uses a Neo4j Knowledge Graph exclusively.

# Setup

1. Ensure the `.env` file has been configured as described in the main [README](../README.md).

This README covers instructions on how to run the Neo4j:
- Locally with Neo4j Desktop
- In a Docker Container

For ease of use, we would recommended that you run the entire application using **Docker Compose** instead. See main [README](../README.md).

If you would prefer not to use **Docker Compose**, read on...

## Using Neo4j Desktop

This can be downloaded [here](https://neo4j.com/download/)

Once installed follow the steps below:

1. Create new project to host your DBMS.
2. Create a new database within the project.
3. Add the username and password to the root `.env` file.
4. Add the database uri to the `.env` file. The default value for this is `bolt://localhost:7687`
5. Run the database in Neo4j desktop.
6. Test the connection is working by asking InferGPT the keyphrase "healthcheck". 
It will return with a status update on the state of the backend and database
7. Load the data located at data/create_graph.cypher into the database and run it

## Running Neo4j in a Docker Container

1. Build the Docker image

```bash
docker build -t {my-data-image-name} .
```

2. Run the backend within a Docker container

```bash
docker run -e NEO4J_AUTH=neo4j/password -p 7474:7474 -p 7687:7687 {my-data-image-name}
```

> Replace `neo4j/password` with your chosen username and password (seperated by a `/`).

3. Check neo4j is running at [http://localhost:7474/](http://localhost:7474/)

## Initial Data (Azure Blob Storage)

To load initial dummy data into the project, you will need an azure blob storage set up, containing a `json` file. 

The following environment variables should be set up:

```
AZURE_STORAGE_CONNECTION_STRING="my-connection-string"
AZURE_STORAGE_CONTAINER_NAME=my-container-name
AZURE_INITIAL_DATA_FILENAME=test-data.json
```

If there is no blob storage set up, it will default to importing no data.

