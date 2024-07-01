import pytest
from fastapi.websockets import WebSocketState
from src.api.connection_manager import ConnectionManager

error_message = "Test Error"


async def async_error(_):
    raise Exception(error_message)


@pytest.fixture
def connection_manager(mocker):
    manager = ConnectionManager()
    mock_ws = mocker.AsyncMock()
    mock_ws.accept = mocker.AsyncMock()
    mock_on_message = mocker.AsyncMock
    mocker.patch.object(manager, "_ConnectionManager__on_message", new_callable=mock_on_message)

    return manager, mock_ws, mock_on_message


@pytest.mark.asyncio
async def test_connect_new_websocket(connection_manager):
    manager, mock_ws, _ = connection_manager

    await manager.connect(mock_ws)

    assert manager.websocket == mock_ws
    mock_ws.accept.assert_awaited_once()


@pytest.mark.asyncio
async def test_connect_websocket_exists(mocker):
    connection_manager = ConnectionManager()
    connection_manager.websocket = mocker.AsyncMock()

    with pytest.raises(Exception) as error:
        await connection_manager.connect(mocker.AsyncMock())

    assert str(error.value) == "Connection already exists"


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

    await manager.disconnect()

    mock_ws.close.assert_awaited_once()
    assert manager.websocket is None


@pytest.mark.asyncio
async def test_disconnect_websocket_no_websocket(connection_manager):
    manager, mock_ws, _ = connection_manager

    await manager.disconnect()

    mock_ws.close.assert_not_called()
    assert manager.websocket is None


@pytest.mark.asyncio
async def test_disconnect_websocket_already_disconnected(connection_manager):
    manager, mock_ws, _ = connection_manager
    mock_ws.client_state = WebSocketState.DISCONNECTED

    await manager.disconnect()

    mock_ws.close.assert_not_called()
    assert manager.websocket is None
