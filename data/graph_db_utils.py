import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

driver = GraphDatabase.driver(URI, auth=AUTH)

def test_connection():
    try:
        driver.verify_connectivity()
        print("database connection active")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        driver.close()
        


def create_node(name, description):
    try:
        session = driver.session()
        query = """
        CREATE (g:Goal {name: $name, description: $description})
        RETURN g
        """
        result = session.run(query, name=name, description=description)
        for record in result:
            print(f"Created goal node: {record['g']}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if session:
            session.close()
        driver.close()
            
            