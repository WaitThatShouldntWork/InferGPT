import asyncio
import logging
import uuid
from src.websockets.types import Message, MessageTypes
from .connection_manager import connection_manager
from src.websockets.confirmations_manager import ConfirmationsManager

logger = logging.getLogger(__name__)


class UserConfirmer:
    _POLL_RATE_SECONDS = 0.5
    _TIMEOUT_SECONDS = 60.0
    _CONFIRMATIONS_MANAGER: ConfirmationsManager

    def __init__(self, manager: ConfirmationsManager):
        self.confirmations_manager = manager

    async def confirm(self, msg: str) -> bool:
        id = uuid.uuid4()
        self.confirmations_manager.add_confirmation(id)
        await self._send_confirmation(id, msg)
        try:
            async with asyncio.timeout(self._TIMEOUT_SECONDS):
                return await self._check_confirmed(id)
        except TimeoutError:
            logger.warning(f"Confirmation with id {id} timed out.")
            self.confirmations_manager.delete_confirmation(id)
            return False

    async def _check_confirmed(self, id: uuid.UUID) -> bool:
        while True:
            try:
                state = self.confirmations_manager.get_confirmation_state(id)
                if isinstance(state, bool):
                    self.confirmations_manager.delete_confirmation(id)
                    return state
            except Exception:
                return False
            await asyncio.sleep(self._POLL_RATE_SECONDS)

    async def _send_confirmation(self, id: uuid.UUID, msg: str):
        data = f"{str(id)}:{msg}"
        message = Message(MessageTypes.CONFIRMATION, data)
        await connection_manager.broadcast(message)
