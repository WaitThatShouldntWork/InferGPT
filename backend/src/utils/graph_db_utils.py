import logging
from neo4j import GraphDatabase
from src.utils import Config
from src.utils.annual_cypher_import import remove_connecting_nodes, remove_transactions_without_merchant, remove_credits

logger = logging.getLogger(__name__)

config = Config()

URI = config.neo4j_uri
AUTH = (config.neo4j_user, config.neo4j_password)

driver = GraphDatabase.driver(URI, auth=AUTH)


def test_connection():
    logger.info("testing database connection...")
    connection_healthy = False
    try:
        driver.verify_connectivity()
        logger.info("database connection verified")
        connection_healthy = True

    except Exception as e:
        logger.critical("database connection failed")
        logger.critical(e)

    finally:
        driver.close()
        return connection_healthy


def execute_query(llm_query):
    try:
        session = driver.session()
        query = llm_query
        records = session.run(query)
        record_dict = [record.data() for record in records]
        return record_dict

    except Exception as e:
        logger.exception(f"Error: {e}")
        raise

    finally:
        if session:
            session.close()
        driver.close()


def populate_db(query, data) -> None:
    data = {"all_data": data}
    try:
        with driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Cleared database")

            session.run(query, data=data)
            logger.info("Database populated")

            session.run(remove_credits)
            logger.info("Removed any credits from database")

            session.run(remove_transactions_without_merchant)
            logger.info("Removed transactions without merchant from database")

            session.run(remove_connecting_nodes)
            logger.info("Removed connecting nodes to transactions without merchants")
    except Exception as e:
        logger.exception(f"Error: {e}")
        raise
    finally:
        if session:
            session.close()
        driver.close()
