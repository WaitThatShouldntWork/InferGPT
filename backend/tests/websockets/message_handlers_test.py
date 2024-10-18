import logging
from unittest.mock import Mock, call, patch
from uuid import uuid4
import pytest
from src.websockets.message_handlers import create_on_ping, on_confirmation, pong


def test_on_ping_send_pong(mocker):
    on_ping = create_on_ping()
    mock_ws = mocker.Mock()
    mock_disconnect = mocker.AsyncMock()
    mocked_create_task = mocker.patch("asyncio.create_task")

    on_ping(mock_ws, mock_disconnect, None)

    first_call = mocked_create_task.call_args_list[0]
    assert first_call == call(mock_ws.send_json(pong))


@pytest.mark.asyncio
async def test_on_ping_no_disconnect(mocker):
    on_ping = create_on_ping()
    mock_ws = mocker.AsyncMock()
    mock_disconnect = mocker.AsyncMock()

    on_ping(mock_ws, mock_disconnect, None)

    mock_disconnect.assert_not_awaited()


@pytest.mark.parametrize("input_value,expected_bool", [("y", True), ("n", False)])
@patch("src.websockets.message_handlers.confirmations_manager")
def test_on_confirmation(confirmations_manager_mock, input_value, expected_bool):
    # Arrange
    confirmation_id = uuid4()
    data = f"{confirmation_id}:{input_value}"
    websocket_mock = Mock()
    disconnect_mock = Mock()

    # Act
    on_confirmation(websocket_mock, disconnect_mock, data)

    # Assert
    confirmations_manager_mock.update_confirmation.assert_called_once_with(confirmation_id, expected_bool)


@patch("src.websockets.message_handlers.confirmations_manager")
def test_on_confirmation_data_is_none(confirmations_manager_mock, caplog):
    # Arrange
    websocket_mock = Mock()
    disconnect_mock = Mock()

    # Act
    on_confirmation(websocket_mock, disconnect_mock, None)

    # Assert
    confirmations_manager_mock.update_confirmation.assert_not_called()
    assert (
        "src.websockets.message_handlers",
        logging.WARNING,
        "Confirmation response did not include data",
    ) in caplog.record_tuples


@patch("src.websockets.message_handlers.confirmations_manager")
def test_on_confirmation_seperator_not_present(confirmations_manager_mock, caplog):
    # Arrange
    websocket_mock = Mock()
    disconnect_mock = Mock()
    data = "abc"

    # Act
    on_confirmation(websocket_mock, disconnect_mock, data)

    # Assert
    confirmations_manager_mock.update_confirmation.assert_not_called()
    assert (
        "src.websockets.message_handlers",
        logging.WARNING,
        "Seperator (':') not present in confirmation",
    ) in caplog.record_tuples


@patch("src.websockets.message_handlers.confirmations_manager")
def test_on_confirmation_seperator_id_not_uuid(confirmations_manager_mock, caplog):
    # Arrange
    websocket_mock = Mock()
    disconnect_mock = Mock()
    data = "abc:y"

    # Act
    on_confirmation(websocket_mock, disconnect_mock, data)

    # Assert
    confirmations_manager_mock.update_confirmation.assert_not_called()
    assert ("src.websockets.message_handlers", logging.WARNING, "Received invalid id") in caplog.record_tuples


@pytest.mark.parametrize("input_value", [(""), ("abc")])
@patch("src.websockets.message_handlers.confirmations_manager")
def test_on_confirmation_value_not_valid(confirmations_manager_mock, caplog, input_value):
    # Arrange
    websocket_mock = Mock()
    disconnect_mock = Mock()
    confirmation_id = uuid4()
    data = f"{confirmation_id}:{input_value}"

    # Act
    on_confirmation(websocket_mock, disconnect_mock, data)

    # Assert
    confirmations_manager_mock.update_confirmation.assert_not_called()
    assert ("src.websockets.message_handlers", logging.WARNING, "Received invalid value") in caplog.record_tuples


@patch("src.websockets.message_handlers.confirmations_manager")
def test_on_confirmation_confirmation_manager_raises_exception(confirmations_manager_mock, caplog):
    # Arrange
    confirmation_id = uuid4()
    data = f"{confirmation_id}:y"
    websocket_mock = Mock()
    disconnect_mock = Mock()
    exception_message = "Test Exception Message"
    confirmations_manager_mock.update_confirmation.side_effect = Exception(exception_message)

    # Act
    on_confirmation(websocket_mock, disconnect_mock, data)

    # Assert
    assert (
        "src.websockets.message_handlers",
        logging.WARNING,
        f"Could not update confirmation: '{exception_message}'",
    ) in caplog.record_tuples
