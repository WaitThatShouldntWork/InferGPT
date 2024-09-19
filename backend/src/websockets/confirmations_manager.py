import logging
from typing import Dict
import uuid
from string import Template

logger = logging.getLogger(__name__)


class ConfirmationsManager:
    _open_confirmations: Dict[uuid.UUID, bool | None] = {}
    _ERROR_MESSAGE = Template(" Confirmation with id '$confirmation_id' not found")

    def add_confirmation(self, confirmation_id: uuid.UUID):
        self._open_confirmations[confirmation_id] = None
        logger.info(f"Confirmation Added: {self._open_confirmations}")

    def get_confirmation_state(self, confirmation_id: uuid.UUID) -> bool | None:
        if confirmation_id in self._open_confirmations:
            return self._open_confirmations[confirmation_id]
        else:
            raise Exception(
                "Cannot get confirmation." + self._ERROR_MESSAGE.substitute(confirmation_id=confirmation_id)
            )

    def update_confirmation(self, confirmation_id: uuid.UUID, value: bool):
        if confirmation_id in self._open_confirmations:
            self._open_confirmations[confirmation_id] = value
        else:
            raise Exception(
                "Cannot update confirmation." + self._ERROR_MESSAGE.substitute(confirmation_id=confirmation_id)
            )

    def delete_confirmation(self, confirmation_id: uuid.UUID):
        if confirmation_id in self._open_confirmations:
            del self._open_confirmations[confirmation_id]
            logger.info(f"Confirmation Deleted: {self._open_confirmations}")
        else:
            raise Exception(
                "Cannot delete confirmation." + self._ERROR_MESSAGE.substitute(confirmation_id=confirmation_id)
            )


confirmations_manager = ConfirmationsManager()
