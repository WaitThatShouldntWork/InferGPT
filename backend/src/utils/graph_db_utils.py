import logging
from neo4j import GraphDatabase
from src.utils import Config

config = Config()

URI = config.neo4j_uri
AUTH = (config.neo4j_user, config.neo4j_password)

driver = GraphDatabase.driver(URI, auth=AUTH)


def test_connection():
    logging.info("testing database connection...")
    connection_healthy = False
    try:
        driver.verify_connectivity()
        logging.info("database connection verified")
        connection_healthy = True

    except Exception as e:
        logging.critical("database connection failed")
        logging.critical(e)

    finally:
        driver.close()
        return connection_healthy
