from unittest.mock import call
import pytest
from src.api.message_handlers import create_on_ping, pong


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
