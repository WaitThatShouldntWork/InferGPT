import pytest
from unittest.mock import patch, AsyncMock
import json
from src.agents.web_agent import web_general_search_core

@pytest.mark.asyncio
@patch("src.agents.web_agent.answer_user_ques", new_callable=AsyncMock)
@patch("src.agents.web_agent.create_search_term", new_callable=AsyncMock)
@patch("src.agents.web_agent.perform_search", new_callable=AsyncMock)
@patch("src.agents.web_agent.perform_scrape", new_callable=AsyncMock)
@patch("src.agents.web_agent.perform_summarization", new_callable=AsyncMock)
@patch("src.agents.web_agent.is_valid_answer", new_callable=AsyncMock)
async def test_web_general_search_core(
    mock_is_valid_answer,
    mock_perform_summarization,
    mock_perform_scrape,
    mock_perform_search,
    mock_create_search_term,
    mock_answer_user_ques
):
    llm = AsyncMock()
    model = "mock_model"

    # Mocking answer_user_ques to return a valid answer
    mock_answer_user_ques.return_value = json.dumps({
        "status": "success",
        "response": json.dumps({"is_valid": True, "answer": "Example summary."})
    })

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

    expected_response = {
        "content": "Error in finding the answer.",
        "ignore_validation": "false"
    }
    assert json.loads(result) == expected_response

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
    mock_perform_summarization.return_value = json.dumps({"summary": "Example invalid summary."})
    mock_is_valid_answer.return_value = False
    result = await web_general_search_core("example query", llm, model)
    expected_response = {
        "content": "Error in finding the answer.",
        "ignore_validation": "false"
    }
    assert json.loads(result) == expected_response

