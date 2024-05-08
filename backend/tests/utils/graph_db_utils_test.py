from unittest.mock import MagicMock
from neo4j import Driver, Session
import pytest

# We assign an alias to "test_connection" to avoid pytest treating it as another test function
from src.utils import test_connection as verify_connection


@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_driver(mocker, mock_session):
    mock_driver = mocker.patch("src.utils.graph_db_utils.driver", return_value=MagicMock(spec=Driver))
    mock_driver.session.return_value = mock_session
    return mock_driver


def remove_whitespace_and_newlines(original):
    return " ".join(original.replace(r"\n", " ").replace(r"\r", "").split())


def test_database_connectivity_is_healthy(mock_driver):
    mock_driver.verify_connectivity.return_value = None

    connected = verify_connection()

    assert connected
    mock_driver.verify_connectivity.assert_called_once()
    mock_driver.close.assert_called_once()


def test_database_connectivity_is_unhealthy(mock_driver):
    mock_driver.verify_connectivity.side_effect = Exception

    connected = verify_connection()

    assert not connected
    mock_driver.verify_connectivity.assert_called_once()
    mock_driver.close.assert_called_once()
