import logging
import pytest
from unittest.mock import Mock, patch
from src.utils.user_logger import user_log, user_log_info
from src.websockets.types import Message, MessageTypes

@pytest.mark.asyncio
async def test_user_log_logger_and_connection_manager_called():
    with patch("src.websockets.connection_manager.ConnectionManager.broadcast") as broadcast:
        logger_mock = Mock()
        with patch("logging.getLogger", return_value=logger_mock) as logging_func:
            test_message = "Test Message"
            test_name = "Test Name"
            await user_log(test_message, logging.INFO, test_name)

            logging_func.assert_called_once_with(test_name)
            logger_mock.log.assert_called_once_with(logging.INFO, f"USER - {test_message}")
            broadcast.assert_awaited_once_with(Message(MessageTypes.LOG, test_message))

@patch("src.utils.user_logger.user_log_info_async")
def test_user_log_info_does_not_call_async_method_if_outside_async_context(user_log_info_async):
    test_message = "Test Message"
    test_name = "Test Name"
    user_log_info(test_message, test_name)

    assert not user_log_info_async.called
