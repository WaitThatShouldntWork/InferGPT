import pytest
from unittest.mock import MagicMock
from neo4j import Driver, Session
from src.utils.graph_db_utils import populate_db
from src.utils import test_connection as verify_connection


@pytest.fixture
def mock_session():
    session = MagicMock(spec=Session)
    session.run = MagicMock()
    session.close = MagicMock()
    return session


@pytest.fixture
def mock_driver(mock_session):
    driver = MagicMock(spec=Driver)
    driver.session.return_value.__enter__.return_value = mock_session
    driver.session.return_value.__exit__.return_value = None
    driver.close = MagicMock()
    return driver


def remove_whitespace_and_newlines(original):
    return " ".join(original.replace(r"\n", " ").replace(r"\r", "").split())


def test_database_connectivity_is_healthy(mocker, mock_driver):
    mocker.patch("src.utils.graph_db_utils.driver", mock_driver)
    mock_driver.verify_connectivity.return_value = None

    connected = verify_connection()

    assert connected
    mock_driver.verify_connectivity.assert_called_once()
    mock_driver.close.assert_called_once()


def test_database_connectivity_is_unhealthy(mocker, mock_driver):
    mocker.patch("src.utils.graph_db_utils.driver", mock_driver)
    mock_driver.verify_connectivity.side_effect = Exception

    connected = verify_connection()

    assert not connected
    mock_driver.verify_connectivity.assert_called_once()
    mock_driver.close.assert_called_once()


def test_populate_db_populates_db(mocker, mock_driver, mock_session):
    mocker.patch("src.utils.graph_db_utils.driver", mock_driver)

    query = "CREATE (n:Test {data: $all_data})"
    data = {"key": "value"}
    remove_credits = "REMOVE CREDITS"
    remove_transactions_without_merchant = "REMOVE TRANSACTIONS"
    remove_connecting_nodes = "REMOVE NODES"

    mocker.patch("src.utils.graph_db_utils.remove_credits", remove_credits)
    mocker.patch("src.utils.graph_db_utils.remove_transactions_without_merchant", remove_transactions_without_merchant)
    mocker.patch("src.utils.graph_db_utils.remove_connecting_nodes", remove_connecting_nodes)

    populate_db(query, data)

    mock_session.run.assert_any_call("MATCH (n) DETACH DELETE n")
    mock_session.run.assert_any_call(query, data={"all_data": data})
    mock_session.run.assert_any_call(remove_credits)
    mock_session.run.assert_any_call(remove_transactions_without_merchant)
    mock_session.run.assert_any_call(remove_connecting_nodes)

    mock_driver.session.return_value.__exit__.assert_called_once()
    mock_driver.close.assert_called_once()


def test_populate_db_throws_exception(mocker, mock_driver, mock_session):
    mocker.patch("src.utils.graph_db_utils.driver", mock_driver)

    query = "CREATE (n:Test {data: $all_data})"
    data = {"key": "value"}

    mock_session.run.side_effect = Exception("Test exception")

    with pytest.raises(Exception, match="Test exception"):
        populate_db(query, data)

    mock_driver.session.return_value.__exit__.assert_called_once()
    mock_driver.close.assert_called_once()
