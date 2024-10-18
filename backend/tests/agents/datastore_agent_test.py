import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.agents.datastore_agent import generate_cypher_query_core

@pytest.mark.asyncio
@patch("src.agents.datastore_agent.get_semantic_layer", new_callable=AsyncMock)
@patch("src.agents.datastore_agent.execute_query", new_callable=MagicMock)
@patch("src.agents.datastore_agent.publish_log_info", new_callable=AsyncMock)
@patch("src.agents.datastore_agent.engine.load_prompt", autospec=True)
async def test_generate_query_success(mock_load_prompt, mock_publish_log_info,
                                      mock_execute_query, mock_get_semantic_layer):
    llm = AsyncMock()
    model = "mock_model"

    mock_load_prompt.side_effect = [
        "details to create cypher query prompt",
        "generate cypher query prompt"
    ]

    llm.chat.return_value = '{"query": "MATCH (n) RETURN n"}'

    mock_get_semantic_layer.return_value = {"nodes": [], "edges": []}

    mock_execute_query.return_value = "Mocked response from the database"

    question_intent = "Find all nodes"
    operation = "MATCH"
    question_params = "n"
    aggregation = "none"
    sort_order = "none"
    timeframe = "2024"
    model = "gpt-4"

    result = await generate_cypher_query_core(question_intent, operation, question_params, aggregation, sort_order,
                                              timeframe, llm, model)

    assert result == '{\n    "content": "Mocked response from the database",\n    "ignore_validation": "false"\n}'
    mock_load_prompt.assert_called()
    llm.chat.assert_called_once_with(
        model,
        "generate cypher query prompt",
        "details to create cypher query prompt",
        return_json=True
    )
    mock_execute_query.assert_called_once_with("MATCH (n) RETURN n")
    mock_publish_log_info.assert_called()

@pytest.mark.asyncio
@patch("src.agents.datastore_agent.get_semantic_layer", new_callable=AsyncMock)
@patch("src.agents.datastore_agent.execute_query", new_callable=MagicMock)
@patch("src.agents.datastore_agent.publish_log_info", new_callable=AsyncMock)
@patch("src.agents.datastore_agent.engine.load_prompt", autospec=True)
async def test_generate_query_failure(mock_load_prompt, mock_publish_log_info,
                                      mock_execute_query, mock_get_semantic_layer):
    llm = AsyncMock()
    model = "mock_model"

    mock_load_prompt.side_effect = [
        "details to create cypher query prompt",
        "generate cypher query prompt"
    ]

    llm.chat.side_effect = Exception("LLM chat failed")

    mock_get_semantic_layer.return_value = {"nodes": [], "edges": []}

    question_intent = "Find all nodes"
    operation = "MATCH"
    question_params = "n"
    aggregation = "none"
    sort_order = "none"
    timeframe = "2024"
    model = "gpt-4"

    with pytest.raises(Exception, match="LLM chat failed"):
        await generate_cypher_query_core(question_intent, operation, question_params, aggregation, sort_order,
                                         timeframe, llm, model)

    mock_load_prompt.assert_called()
    llm.chat.assert_called_once_with(
        model,
        "generate cypher query prompt",
        "details to create cypher query prompt",
        return_json=True
    )
    mock_publish_log_info.assert_not_called()
    mock_execute_query.assert_not_called()

if __name__ == "__main__":
    pytest.main(["-v"])
