from fastapi.testclient import TestClient
from api import app, healthy_response, error_message

client = TestClient(app)
utterance = "Hello there"

def test_health_check_response():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == healthy_response

def test_chat_success_response(mocker):
    expected_message = 'InferGPT backend is healthy'
    mock_question = mocker.patch('api.question', return_value=expected_message)

    response = client.get(f"/chat?utterance={utterance}")

    mock_question.assert_called_with(utterance)
    assert response.status_code == 200
    assert response.json() == expected_message

def test_chat_failure_response(mocker):
    expected_message = 'InferGPT backend is healthy'
    mock_question = mocker.patch('api.question', return_value=expected_message)
    mock_question.side_effect = Exception('An error occurred')

    response = client.get(f"/chat?utterance={utterance}")

    mock_question.assert_called_with(utterance)
    assert response.status_code == 500
    assert response.json() == error_message
