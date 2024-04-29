from unittest.mock import ANY, MagicMock
from neo4j import Driver, Session
import pytest
import utils.graph_db_utils

def test_database_connectivity_is_healthy(mocker):
    mock_driver = mocker.patch("utils.graph_db_utils.driver", return_value=MagicMock(spec=Driver))
    mock_driver.verify_connectivity.return_value = None

    connectivity = utils.graph_db_utils.test_connection()

    assert connectivity
    mock_driver.verify_connectivity.assert_called_once()
    mock_driver.close.assert_called_once()


def test_database_connectivity_is_unhealthy(mocker):
    mock_driver = mocker.patch("utils.graph_db_utils.driver", return_value=MagicMock(spec=Driver))
    mock_driver.verify_connectivity.side_effect = Exception

    connectivity = utils.graph_db_utils.test_connection()

    assert not connectivity
    mock_driver.verify_connectivity.assert_called_once()
    mock_driver.close.assert_called_once()


def test_create_goal_is_successful(mocker):
    mock_driver = mocker.patch("utils.graph_db_utils.driver", return_value=MagicMock(spec=Driver))
    mock_session = MagicMock(spec=Session)
    mock_driver.session.return_value = mock_session

    response = utils.graph_db_utils.create_goal("Test Name", "Test Description")

    assert response is None
    mock_session.run.assert_called_once_with(ANY, name="Test Name", description="Test Description")
    mock_session.close.assert_called_once()
    mock_driver.close.assert_called_once()


def test_create_goal_throws_exception(mocker):
    mock_driver = mocker.patch("utils.graph_db_utils.driver", return_value=MagicMock(spec=Driver))
    mock_session = MagicMock(spec=Session)
    mock_driver.session.return_value = mock_session
    mock_session.run.side_effect = Exception

    with pytest.raises(Exception):
        utils.graph_db_utils.create_goal("Test Name", "Test Description")

    mock_session.run.assert_called_once_with(ANY, name="Test Name", description="Test Description")
    mock_session.close.assert_called_once()
    mock_driver.close.assert_called_once()
