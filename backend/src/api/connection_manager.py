import logging
from typing import Any, Dict
from fastapi import WebSocket
from fastapi.websockets import WebSocketState

from .types import Message, MessageTypes
from .message_handlers import handlers


def parse_message(message: Dict[str, Any]) -> Message:
    data = message.get("data") or None
    return Message(type=message["type"], data=data)


class ConnectionManager:
    websocket: WebSocket | None

    def __init__(self):
        self.websocket = None

    async def __handle_message(self, message: Message):
        handler = handlers.get(MessageTypes(message.type))
        if handler is None:
            raise Exception("No handler for message type")

        if self.websocket is not None:
            handler(self.websocket, self.disconnect, message.data)

    async def __on_message(self):
        if self.websocket is None:
            raise Exception("No connection")

        raw_message = await self.websocket.receive_json()
        parsed_message = parse_message(raw_message)

        await self.__handle_message(parsed_message)
        await self.__on_message()

    async def connect(self, websocket: WebSocket):
        if self.websocket is not None:
            raise Exception("Connection already exists")

        await websocket.accept()
        self.websocket = websocket
        try:
            await self.__on_message()
        except Exception as e:
            logging.error(f"Error in process: {e}")
            await self.disconnect()

    async def disconnect(self):
        if self.websocket is not None and self.websocket.client_state != WebSocketState.DISCONNECTED:
            await self.websocket.close()
        self.websocket = None
