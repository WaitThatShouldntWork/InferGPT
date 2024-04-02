import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

def test_connection():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("database connection active")
        
    driver.close()


def create_node(name, description):
    driver = GraphDatabase.driver(URI, auth=AUTH)
    
    with driver.session() as session:
        query = """
        CREATE (g:Goal {name: $name, description: $description})
        RETURN g
        """
        result = session.run(query, name=name, description=description)
        for record in result:
            print(f"Created goal node: {record['g']}")

    driver.close()
        