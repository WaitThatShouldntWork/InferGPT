import logging
from unittest.mock import Mock, patch

import pytest

from src.websockets.types import Message, MessageTypes
from src.websockets.user_confirmer import UserConfirmer
from src.websockets.confirmations_manager import ConfirmationsManager


class TestUserConfirmer:
    @pytest.mark.asyncio
    async def test_confirm_times_out(self, caplog):
        # Arrange
        confirmations_manager_mock = Mock(spec=ConfirmationsManager)
        confirmations_manager_mock.get_confirmation_state.return_value = None
        user_confirmer = UserConfirmer(confirmations_manager_mock)
        user_confirmer._TIMEOUT_SECONDS = 0.05
        user_confirmer._POLL_RATE_SECONDS = 0.01

        # Act
        result = await user_confirmer.confirm("Test Message")

        # Assert
        assert result is False
        confirmations_manager_mock.add_confirmation.assert_called_once()
        id = confirmations_manager_mock.add_confirmation.call_args.args[0]
        confirmations_manager_mock.delete_confirmation.assert_called_once_with(id)
        assert caplog.record_tuples == [
            ("src.websockets.user_confirmer", logging.WARNING, f"Confirmation with id {id} timed out.")
        ]

    @pytest.mark.asyncio
    @patch("src.websockets.connection_manager.connection_manager")
    async def test_confirm_approved(self, connection_manager_mock):
        # Arrange
        confirmations_manager_mock = Mock(spec=ConfirmationsManager)
        confirmations_manager_mock.get_confirmation_state.side_effect = [None, True]
        user_confirmer = UserConfirmer(confirmations_manager_mock)
        user_confirmer._POLL_RATE_SECONDS = 0.01

        # Act
        result = await user_confirmer.confirm("Test Message")

        # Assert
        assert result is True
        confirmations_manager_mock.add_confirmation.assert_called_once()
        id = confirmations_manager_mock.add_confirmation.call_args.args[0]
        connection_manager_mock.broadcast.awaited_once_with(Message(MessageTypes.CONFIRMATION, f"{id}:Test Message"))
        confirmations_manager_mock.get_confirmation_state.assert_called_with(id)
        assert confirmations_manager_mock.get_confirmation_state.call_count == 2
        confirmations_manager_mock.delete_confirmation.assert_called_once_with(id)

    @pytest.mark.asyncio
    @patch("src.websockets.connection_manager.connection_manager")
    async def test_confirm_denied(self, connection_manager_mock):
        # Arrange
        confirmations_manager_mock = Mock(spec=ConfirmationsManager)
        confirmations_manager_mock.get_confirmation_state.side_effect = [None, False]
        user_confirmer = UserConfirmer(confirmations_manager_mock)
        user_confirmer._POLL_RATE_SECONDS = 0.01

        # Act
        result = await user_confirmer.confirm("Test Message")

        # Assert
        assert result is False
        confirmations_manager_mock.add_confirmation.assert_called_once()
        id = confirmations_manager_mock.add_confirmation.call_args.args[0]
        connection_manager_mock.broadcast.awaited_once_with(Message(MessageTypes.CONFIRMATION, f"{id}:Test Message"))
        confirmations_manager_mock.get_confirmation_state.assert_called_with(id)
        assert confirmations_manager_mock.get_confirmation_state.call_count == 2
        confirmations_manager_mock.delete_confirmation.assert_called_once_with(id)
