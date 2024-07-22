import json
import logging
from typing import Any, Dict, List
from fastapi import WebSocket
from fastapi.websockets import WebSocketState

from .types import Message, MessageTypes
from .message_handlers import handlers

logger = logging.getLogger(__name__)

def parse_message(message: Dict[str, Any]) -> Message:
    data = message.get("data") or None
    return Message(type=message["type"], data=data)


class ConnectionManager:
    websockets: List[WebSocket]

    def __init__(self):
        self.websockets = []

    async def connect(self, ws: WebSocket):
        if ws not in self.websockets:
            await ws.accept()
            self.websockets.append(ws)
        else:
            raise Exception(f"Given websocket ({ws}) was already being tracked")

    async def disconnect(self, ws: WebSocket):
        try:
            self.websockets.remove(ws)
            if ws.client_state != WebSocketState.DISCONNECTED:
                await ws.close()
        except ValueError:
            pass

    async def handle_message(self, ws: WebSocket, message: Message):
        handler = handlers.get(MessageTypes(message.type))
        if handler is None:
            raise Exception("No handler for message type")
        handler(ws, self.disconnect, message.data)

    # This broadcast method is a place holder until the backend has implemented the idea of a user session
    # at that point this should be replaced by a send message that targets a specific web socket.
    async def broadcast(self, message: Message):
        for ws in self.websockets:
            if ws.application_state == WebSocketState.CONNECTED:
                await ws.send_json(json.dumps({"type": message.type.value, "data": message.data}))

connection_manager = ConnectionManager()
