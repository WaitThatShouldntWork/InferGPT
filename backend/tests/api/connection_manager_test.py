import json
from unittest.mock import patch
import pytest
from fastapi.websockets import WebSocketState
from src.websockets.types import Message, MessageTypes
from src.websockets.message_handlers import handlers
from src.websockets.connection_manager import ConnectionManager

error_message = "Test Error"


async def async_error(_):
    raise Exception(error_message)


@pytest.fixture
def connection_manager(mocker):
    manager = ConnectionManager()
    mock_ws = mocker.AsyncMock()
    mock_ws.accept = mocker.AsyncMock()
    mock_ws.send_json = mocker.AsyncMock()
    mock_on_message = mocker.AsyncMock

    return manager, mock_ws, mock_on_message


@pytest.mark.asyncio
async def test_connect_new_websocket(connection_manager):
    manager, mock_ws, _ = connection_manager

    await manager.connect(mock_ws)

    assert len(manager.websockets) == 1
    assert manager.websockets[0] == mock_ws
    mock_ws.accept.assert_awaited_once()


@pytest.mark.asyncio
async def test_connect_second_websocket(connection_manager, mocker):
    manager, mock_ws, _ = connection_manager
    manager.websockets.append(mocker.AsyncMock())

    await manager.connect(mock_ws)

    assert len(manager.websockets) == 2
    assert manager.websockets[1] == mock_ws
    mock_ws.accept.assert_awaited_once()


@pytest.mark.asyncio
async def test_connect_websocket_already_in_manager(connection_manager):
    manager, mock_ws, _ = connection_manager
    manager.websockets.append(mock_ws)

    with pytest.raises(Exception) as error:
        await manager.connect(mock_ws)

    assert str(error.value) == f"Given websocket ({mock_ws}) was already being tracked"


@pytest.mark.asyncio
async def test_handle_connect_on_message_error(connection_manager):
    manager, mock_ws, mock_on_message = connection_manager
    mock_on_message.side_effect = async_error

    with pytest.raises(Exception) as error:
        await manager.connect(mock_ws)

    assert str(error.value) == error_message


@pytest.mark.asyncio
async def test_disconnect_websocket_close_connection(connection_manager):
    manager, mock_ws, _ = connection_manager
    await manager.connect(mock_ws)

    await manager.disconnect(mock_ws)

    mock_ws.close.assert_awaited_once()
    assert len(manager.websockets) == 0


@pytest.mark.asyncio
async def test_disconnect_websocket_websocket_not_tracked(connection_manager):
    manager, mock_ws, _ = connection_manager

    await manager.disconnect(mock_ws)

    mock_ws.close.assert_not_called()
    assert len(manager.websockets) == 0


@pytest.mark.asyncio
async def test_disconnect_websocket_already_disconnected(connection_manager):
    manager, mock_ws, _ = connection_manager
    mock_ws.client_state = WebSocketState.DISCONNECTED
    manager.websockets.append(mock_ws)

    await manager.disconnect(mock_ws)

    mock_ws.close.assert_not_called()
    assert len(manager.websockets) == 0

@pytest.mark.asyncio
async def test_handle_message_handler_exists_for_message_type_handler_called(connection_manager, mocker):
    manager, mock_ws, _ = connection_manager
    handler = mocker.Mock()
    with patch.dict(handlers, {MessageTypes.CHAT: handler}):
        message = Message(MessageTypes.CHAT, "Test String")

        await manager.handle_message(mock_ws, message)

        handler.assert_called()



@pytest.mark.asyncio
async def test_handle_message_handler_does_not_exist_for_message_type_handler_called(connection_manager):
    manager, mock_ws, _ = connection_manager
    with patch.dict(handlers, {}):
        message = Message(MessageTypes.PONG, "Test String")

        with pytest.raises(Exception) as error:
            await manager.handle_message(mock_ws, message)

        assert str(error.value) == "No handler for message type"



@pytest.mark.asyncio
async def test_broadcast_given_message_broadcasted(connection_manager):
    manager, mock_ws, _ = connection_manager
    manager.websockets.append(mock_ws)
    mock_ws.application_state = WebSocketState.CONNECTED
    message = Message(MessageTypes.CHAT, "Test String")

    await manager.broadcast(message)

    mock_ws.send_json.assert_awaited_once_with(json.dumps({"type": message.type.value, "data": message.data}))


@pytest.mark.asyncio
async def test_broadcast_given_ws_state_not_connected_message_not_broadcasted(connection_manager):
    manager, mock_ws, _ = connection_manager
    manager.websockets.append(mock_ws)
    mock_ws.application_state = WebSocketState.CONNECTING
    message = Message(MessageTypes.CHAT, "Test String")

    await manager.broadcast(message)

    mock_ws.send_json.assert_not_called()


@pytest.mark.asyncio
async def test_broadcast_no_ws_tracked_broadcast_does_not_throw(connection_manager):
    manager, _, _ = connection_manager
    message = Message(MessageTypes.CHAT, "Test String")

    await manager.broadcast(message)
