import asyncio
import json
import logging
from uuid import UUID
from fastapi import WebSocket
from typing import Callable
from .types import Handlers, MessageTypes
from src.websockets.confirmations_manager import confirmations_manager

logger = logging.getLogger(__name__)

heartbeat_timeout = 30
pong = json.dumps({"type": MessageTypes.PONG.value})


def create_on_ping():
    heartbeat_timer: asyncio.Task | None = None

    async def heartbeat(disconnect: Callable, ws: WebSocket):
        try:
            await asyncio.sleep(heartbeat_timeout)
            await disconnect(ws)
        except asyncio.CancelledError:
            pass

    def on_ping(websocket: WebSocket, disconnect: Callable, data: str | None):
        nonlocal heartbeat_timer

        asyncio.create_task(websocket.send_json(pong))

        if heartbeat_timer is not None:
            heartbeat_timer.cancel()

        heartbeat_timer = asyncio.create_task(heartbeat(disconnect, websocket))

    return on_ping


def on_chat(websocket: WebSocket, disconnect: Callable, data: str | None):
    logger.info(f"Chat message: {data}")


def on_confirmation(websocket: WebSocket, disconnect: Callable, data: str | None):
    if data is None:
        logger.warning("Confirmation response did not include data")
        return
    if ":" not in data:
        logger.warning("Seperator (':') not present in confirmation")
        return
    sections = data.split(":")
    try:
        id = UUID(sections[0])
    except ValueError:
        logger.warning("Received invalid id")
        return
    if sections[1] != "y" and sections[1] != "n":
        logger.warning("Received invalid value")
        return
    try:
        confirmations_manager.update_confirmation(id, sections[1] == "y")
    except Exception as e:
        logger.warning(f"Could not update confirmation: '{e}'")


handlers: Handlers = {
    MessageTypes.PING: create_on_ping(),
    MessageTypes.CHAT: on_chat,
    MessageTypes.CONFIRMATION: on_confirmation,
}
