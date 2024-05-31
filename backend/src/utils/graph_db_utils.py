import logging
from neo4j import GraphDatabase
from src.utils import Config
from src.utils.annual_cypher_import import remove_connecting_nodes, remove_transactions_without_merchant, remove_credits

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


def execute_query(llm_query):
    try:
        session = driver.session()
        query = llm_query
        records = session.run(query)
        record_dict = [record.data() for record in records]
        return record_dict

    except Exception as e:
        logging.exception(f"Error: {e}")
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
            logging.info("Cleared database")

            session.run(query, data=data)
            logging.info("Database populated")

            session.run(remove_credits)
            logging.info("Removed any credits from database")

            session.run(remove_transactions_without_merchant)
            logging.info("Removed transactions without merchant from database")

            session.run(remove_connecting_nodes)
            logging.info("Removed connecting nodes to transactions without merchants")
    except Exception as e:
        logging.exception(f"Error: {e}")
        raise
    finally:
        if session:
            session.close()
        driver.close()


# Function to execute a query on a Neo4j database
def run_query(query):
    try:
        session = driver.session()
        result = session.execute_read(lambda tx: tx.run(query).data())
        return result
    except Exception as e:
        logging.exception(f"Error: {e}")
        raise

    finally:
        if session:
            session.close()
        driver.close()
