import logging
import asyncio
from src.websockets.types import Message, MessageTypes
from src.websockets.connection_manager import connection_manager

log = logging.getLogger(__name__)

async def user_log(msg: str, loglevel: int, name: str):
    logger = logging.getLogger(name)
    formatted_log = f"USER - {msg}"
    logger.log(loglevel, formatted_log)
    message = Message(MessageTypes.LOG, msg)
    await connection_manager.broadcast(message)

async def user_log_info_async(msg: str, name: str):
    await user_log(msg, logging.INFO, name)

def user_log_info(msg: str, name: str):
    try:
        asyncio.get_running_loop()
        asyncio.create_task(user_log_info_async(msg, name))
    except RuntimeError:
        pass
