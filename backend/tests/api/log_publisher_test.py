import logging
import pytest
from unittest.mock import Mock, patch
from src.utils.log_publisher import LogPrefix, publish_log, publish_log_info_async
from src.websockets.types import Message, MessageTypes


@pytest.mark.asyncio
async def test_publish_log_logger_and_connection_manager_called():
    with patch("src.websockets.connection_manager.ConnectionManager.broadcast") as broadcast:
        logger_mock = Mock()
        with patch("logging.getLogger", return_value=logger_mock) as logging_func:
            test_message = "Test Message"
            test_name = "Test Name"
            await publish_log(LogPrefix.USER, test_message, logging.INFO, test_name)

            logging_func.assert_called_once_with(test_name)
            logger_mock.log.assert_called_once_with(logging.INFO, f"USER - {test_message}")
            broadcast.assert_awaited_once_with(Message(MessageTypes.LOG, test_message))


@pytest.mark.asyncio
async def test_publish_log_info_async_publish_log_called():
    with patch("src.utils.log_publisher.publish_log") as publish_log_mock:
        test_message = "Test Message"
        test_name = "Test Name"
        await publish_log_info_async(LogPrefix.USER, test_message, test_name)

        publish_log_mock.assert_awaited_once_with(LogPrefix.USER, test_message, logging.INFO, test_name)
