from fastapi.testclient import TestClient
import pytest
from src.api import app, healthy_response, unhealthy_neo4j_response, chat_fail_response

client = TestClient(app)
utterance = "Hello there"
expected_message = "Hello to you too! From InferGPT"

@pytest.fixture
def mock_initial_data(mocker):
    blob_service_client = mocker.patch("src.api.app.BlobServiceClient", return_value=mocker.Mock())
    container_client = mocker.Mock()
    blob_service_client.get_container_client.return_value = container_client
    blob_client = mocker.Mock()
    container_client.get_blob_client.return_value = blob_client
    download_stream = mocker.Mock()
    blob_client.download_blob.return_value = download_stream
    mock_data = mocker.Mock()
    mocker.patch("src.api.app.json.loads", return_value=mock_data)

    return mock_data

def test_health_check_response_healthy(mocker):
    mock_test_connection = mocker.patch("src.api.app.test_connection", return_value=True)

    response = client.get("/health")

    mock_test_connection.assert_called()
    assert response.status_code == 200
    assert response.json() == healthy_response


def test_health_check_response_neo4j_unhealthy(mocker):
    mock_test_connection = mocker.patch("src.api.app.test_connection", return_value=False)

    response = client.get("/health")

    mock_test_connection.assert_called()
    assert response.status_code == 500
    assert response.json() == unhealthy_neo4j_response


def test_chat_response_success(mocker):
    mock_question = mocker.patch("src.api.app.question", return_value=expected_message)

    response = client.get(f"/chat?utterance={utterance}")

    mock_question.assert_called_with(utterance)
    assert response.status_code == 200
    assert response.json() == expected_message


def test_chat_response_failure(mocker):
    mock_question = mocker.patch("src.api.app.question", return_value=expected_message)
    mock_question.side_effect = Exception("An error occurred")

    response = client.get(f"/chat?utterance={utterance}")

    mock_question.assert_called_with(utterance)
    assert response.status_code == 500
    assert response.json() == chat_fail_response


@pytest.mark.asyncio
async def test_lifespan_populates_db(mocker, mock_initial_data) -> None:
    mock_populate_db = mocker.patch("src.api.app.populate_db", return_value=mocker.Mock())
    mock_annual_transactions_cypher_script = mocker.patch(
        "src.api.app.annual_transactions_cypher_script", return_value=(mocker.Mock())
    )
    mock_config = {
        "azure_initial_data_filename": "test_file",
        "azure_storage_connection_string": "test_connection_string",
        "azure_storage_container_name": "test_container",
    }
    mocker.patch("src.api.app.config", return_value=mock_config)

    with client:
        mock_populate_db.assert_called_once_with(mock_annual_transactions_cypher_script, mock_initial_data)


@pytest.mark.asyncio
async def test_lifespan_missing_config_populates_db(mocker) -> None:
    mock_populate_db = mocker.patch("src.api.app.populate_db", return_value=mocker.Mock())
    mock_annual_transactions_cypher_script = mocker.patch(
        "src.api.app.annual_transactions_cypher_script", return_value=(mocker.Mock())
    )
    mocker.patch("src.api.app.config", None)

    with client:
        mock_populate_db.assert_called_once_with(mock_annual_transactions_cypher_script, {})
