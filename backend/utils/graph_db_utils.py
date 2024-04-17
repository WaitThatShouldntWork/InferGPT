import logging
from utils import Config
from neo4j import GraphDatabase

config = Config()

URI = config.neo4j_uri
AUTH = (config.neo4j_user, config.neo4j_password)

driver = GraphDatabase.driver(URI, auth=AUTH)

def test_connection():
    logging.info("testing database connection...")
    connectionHealthy = False;
    try:
        driver.verify_connectivity()
        logging.info("database connection verified")
        connectionHealthy = True;
        
    except Exception as e:
        logging.critical("connection connection failed")
        logging.critical(e)
        
    finally:
        driver.close()
        return connectionHealthy;
    
def create_goal(name, description):
    try:
        session = driver.session()
        query = """
        MERGE (g:Goal {name: $name, description: $description})
        RETURN g
        """
        session.run(query, name=name, description=description)
        logging.debug("goal created")

    except Exception as e:
        logging.exception(f"Error: {e}")
        raise

    finally:
        if session:
            session.close()
        driver.close()    
