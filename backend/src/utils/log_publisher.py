import logging
import asyncio
from enum import Enum
from src.websockets.types import Message, MessageTypes
from src.websockets.connection_manager import connection_manager

log = logging.getLogger(__name__)

class LogPrefix(Enum):
    USER = "USER"

async def publish_log(prefix: LogPrefix, msg: str, loglevel: int, name: str):
    logger = logging.getLogger(name)
    formatted_log = f"{prefix.value} - {msg}"
    logger.log(loglevel, formatted_log)
    message = Message(MessageTypes.LOG, msg)
    await connection_manager.broadcast(message)

async def publish_log_info_async(prefix: LogPrefix, msg: str, name: str):
    await publish_log(prefix, msg, logging.INFO, name)

def publish_log_info(prefix: LogPrefix, msg: str, name: str):
    try:
        asyncio.get_running_loop()
        asyncio.create_task(publish_log_info_async(prefix, msg, name))
    except RuntimeError:
        pass
