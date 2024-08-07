from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict

from fastapi import WebSocket


class MessageTypes(Enum):
    PING = "ping"
    PONG = "pong"
    CHAT = "chat"
    LOG  = "log"
    CHART = "chart"


@dataclass
class Message:
    type: MessageTypes
    data: str | None


Handler = Callable[[WebSocket, Callable, str | None], None]
Handlers = Dict[MessageTypes, Handler]
