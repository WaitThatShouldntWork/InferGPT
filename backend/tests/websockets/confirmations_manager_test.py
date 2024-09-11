from uuid import uuid4

import pytest
from src.websockets.confirmations_manager import ConfirmationsManager


class TestConfirmationsManager:
    def test_add_confirmation(self):
        # Arrange
        manager = ConfirmationsManager()
        confirmation_id = uuid4()

        # Act
        manager.add_confirmation(confirmation_id)

        # Assert
        confirmation = manager.get_confirmation_state(confirmation_id)
        assert confirmation is None

    def test_get_confirmation_state_not_found_id(self):
        # Arrange
        manager = ConfirmationsManager()
        not_found_confirmation_id = uuid4()

        # Act
        with pytest.raises(Exception) as e:
            manager.get_confirmation_state(not_found_confirmation_id)

        # Assert
        assert str(e.value) == f"Cannot get confirmation. Confirmation with id '{not_found_confirmation_id}' not found"

    @pytest.mark.parametrize("input_value", [True, False])
    def test_update_confirmation(self, input_value):
        # Arrange
        manager = ConfirmationsManager()
        confirmation_id = uuid4()
        manager.add_confirmation(confirmation_id)

        # Act
        manager.update_confirmation(confirmation_id, input_value)

        # Assert
        updated_value = manager.get_confirmation_state(confirmation_id)
        assert updated_value == input_value

    def test_update_confirmation_not_found_id(self):
        # Arrange
        manager = ConfirmationsManager()
        not_found_confirmation_id = uuid4()

        # Act
        with pytest.raises(Exception) as e:
            manager.update_confirmation(not_found_confirmation_id, True)

        # Assert
        assert (
            str(e.value) == f"Cannot update confirmation. Confirmation with id '{not_found_confirmation_id}' not found"
        )

    def test_delete_confirmation(self):
        # Arrange
        manager = ConfirmationsManager()
        confirmation_id = uuid4()
        manager.add_confirmation(confirmation_id)

        # Act
        manager.delete_confirmation(confirmation_id)

        # Assert
        with pytest.raises(Exception) as e:
            manager.get_confirmation_state(confirmation_id)
        assert "Cannot get confirmation." in str(e.value)

    def test_delete_confirmation_not_found_id(self):
        # Arrange
        manager = ConfirmationsManager()
        not_found_confirmation_id = uuid4()

        # Act
        with pytest.raises(Exception) as e:
            manager.delete_confirmation(not_found_confirmation_id)

        # Assert
        assert (
            str(e.value) == f"Cannot delete confirmation. Confirmation with id '{not_found_confirmation_id}' not found"
        )
