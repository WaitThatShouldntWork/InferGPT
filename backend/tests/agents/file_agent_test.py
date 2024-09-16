import pytest
from unittest.mock import patch, mock_open
import json
import os
from src.agents.file_agent import read_file_core, write_file_core

# Mocking config for the test
@pytest.fixture(autouse=True)
def mock_config(monkeypatch):
    monkeypatch.setattr('src.agents.file_agent.config.files_directory', 'files')

@pytest.mark.asyncio
@patch("builtins.open", new_callable=mock_open, read_data="Example file content.")
async def test_read_file_core_success(mock_file):
    file_path = "example.txt"
    result = await read_file_core(file_path)
    expected_response = {
        "content": "Example file content.",
        "ignore_validation": "true"
    }
    assert json.loads(result) == expected_response
    expected_full_path = os.path.normpath("/app/files/example.txt")
    mock_file.assert_called_once_with(expected_full_path, 'r')

@pytest.mark.asyncio
@patch("builtins.open", side_effect=FileNotFoundError)
async def test_read_file_core_file_not_found(mock_file):
    file_path = "missing_file.txt"
    result = await read_file_core(file_path)
    expected_response = {
        "content": "File missing_file.txt not found.",
        "ignore_validation": "error"
    }
    assert json.loads(result) == expected_response
    expected_full_path = os.path.normpath("/app/files/missing_file.txt")
    mock_file.assert_called_once_with(expected_full_path, 'r')

@pytest.mark.asyncio
@patch("builtins.open", new_callable=mock_open)
async def test_write_file_core_success(mock_file):
    file_path = "example_write.txt"
    content = "This is test content to write."
    result = await write_file_core(file_path, content)
    expected_response = {
        "content": f"Content written to file {file_path}.",
        "ignore_validation": "true"
    }
    assert json.loads(result) == expected_response
    expected_full_path = os.path.normpath("/app/files/example_write.txt")
    mock_file.assert_called_once_with(expected_full_path, 'w')
    mock_file().write.assert_called_once_with(content)

@pytest.mark.asyncio
@patch("builtins.open", side_effect=Exception("Unexpected error"))
async def test_write_file_core_error(mock_file):
    file_path = "error_file.txt"
    content = "Content with error."
    result = await write_file_core(file_path, content)
    expected_response = {
        "status": "error",
        "message": "Error writing to file: Unexpected error"
    }
    assert json.loads(result) == expected_response
    expected_full_path = os.path.normpath("/app/files/error_file.txt")
    mock_file.assert_called_once_with(expected_full_path, 'w')
