import os
import logging
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

driver = GraphDatabase.driver(URI, auth=AUTH)

def test_connection():
    try:
        driver.verify_connectivity()
        logging.debug("database connection active")
        
    except Exception as e:
        logging.exception(f"Error: {e}")
        raise
        
    finally:
        driver.close()
    
def create_goal(name, description):
    try:
        session = driver.session()
        query = """
        MERGE (g:Goal {name: $name, description: $description})
        RETURN g
        """
        result = session.run(query, name=name, description=description)
        logging.debug("goal created")

    except Exception as e:
        logging.exception(f"Error: {e}")
        raise

    finally:
        if session:
            session.close()
        driver.close()    
