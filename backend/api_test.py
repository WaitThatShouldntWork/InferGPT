from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from api import app, healthy_response, unhealthy_backend_response, unhealthy_neo4j_response, chat_fail_response

client = TestClient(app)
utterance = "Hello there"
expected_message = "Hello to you too! From InferGPT"

# TODO: Neo4J Desktop needs running for these tests to work
#       - consider implementing a Neo4J database embedded as part of running the tests to remove this dependency

def test_health_check_response_healthy():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == healthy_response

def test_health_check_response_neo4j_unhealthy(mocker):
    mock_connection_test = mocker.patch("api.test_connection", return_value=False)

    response = client.get("/health")

    mock_connection_test.assert_called()

    assert response.status_code == 500
    assert response.json() == unhealthy_neo4j_response

def test_chat_response_success(mocker):
    mock_question = mocker.patch("api.question", return_value=expected_message)

    response = client.get(f"/chat?utterance={utterance}")

    mock_question.assert_called_with(utterance)
    assert response.status_code == 200
    assert response.json() == expected_message


def test_chat_response(mocker):
    mock_question = mocker.patch("api.question", return_value=expected_message)
    mock_question.side_effect = Exception("An error occurred")

    response = client.get(f"/chat?utterance={utterance}")

    mock_question.assert_called_with(utterance)
    assert response.status_code == 500
    assert response.json() == chat_fail_response
