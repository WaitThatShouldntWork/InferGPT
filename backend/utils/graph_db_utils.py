import logging
from utils import Config
from neo4j import GraphDatabase

config = Config()

URI = config.neo4j_uri
AUTH = (config.neo4j_user, config.neo4j_password)

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
