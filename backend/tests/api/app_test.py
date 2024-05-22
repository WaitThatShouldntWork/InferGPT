from fastapi.testclient import TestClient
from src.api import app, healthy_response, unhealthy_neo4j_response, chat_fail_response

client = TestClient(app)
utterance = "Hello there"
expected_message = "Hello to you too! From InferGPT"


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
