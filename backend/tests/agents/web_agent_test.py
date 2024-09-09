import unittest
from unittest.mock import AsyncMock, patch
import json

import pytest
from src.agents.web_agent import web_general_search_core

@pytest.mark.asyncio
@patch("src.agents.web_agent.perform_search", new_callable=AsyncMock)
@patch("src.agents.web_agent.perform_scrape", new_callable=AsyncMock)
@patch("src.agents.web_agent.perform_summarization", new_callable=AsyncMock)
@patch("src.agents.web_agent.is_valid_answer", new_callable=AsyncMock)
async def test_web_general_search_core(
    mock_is_valid_answer,
    mock_perform_summarization,
    mock_perform_scrape,
    mock_perform_search,
):
    llm = AsyncMock()
    model = "mock_model"

    mock_perform_search.return_value = {"status": "success", "urls": ["http://example.com"]}
    mock_perform_scrape.return_value = "Example scraped content."
    mock_perform_summarization.return_value = "Example summary."
    mock_is_valid_answer.return_value = True
    result = await web_general_search_core("example query", llm, model)
    expected_response = {
        "content": "Example summary.",
        "ignore_validation": "false"
    }
    assert json.loads(result) == expected_response

@pytest.mark.asyncio
@patch("src.agents.web_agent.perform_search", new_callable=AsyncMock)
@patch("src.agents.web_agent.perform_scrape", new_callable=AsyncMock)
@patch("src.agents.web_agent.perform_summarization", new_callable=AsyncMock)
@patch("src.agents.web_agent.is_valid_answer", new_callable=AsyncMock)
async def test_web_general_search_core_no_results(
    mock_is_valid_answer,
    mock_perform_summarization,
    mock_perform_scrape,
    mock_perform_search,
):
    llm = AsyncMock()
    model = "mock_model"
    mock_perform_search.return_value = {"status": "error", "urls": []}
    result = await web_general_search_core("example query", llm, model)
    assert result == "No relevant information found on the internet for the given query."


@pytest.mark.asyncio
@patch("src.agents.web_agent.perform_search", new_callable=AsyncMock)
@patch("src.agents.web_agent.perform_scrape", new_callable=AsyncMock)
@patch("src.agents.web_agent.perform_summarization", new_callable=AsyncMock)
@patch("src.agents.web_agent.is_valid_answer", new_callable=AsyncMock)
async def test_web_general_search_core_invalid_summary(
    mock_is_valid_answer,
    mock_perform_summarization,
    mock_perform_scrape,
    mock_perform_search
):
    llm = AsyncMock()
    model = "mock_model"
    mock_perform_search.return_value = {"status": "success", "urls": ["http://example.com"]}
    mock_perform_scrape.return_value = "Example scraped content."
    mock_perform_summarization.return_value = "Example invalid summary."
    mock_is_valid_answer.return_value = False
    result = await web_general_search_core("example query", llm, model)
    assert result == "No relevant information found on the internet for the given query."
