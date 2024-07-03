from src.api import app
from fastapi.testclient import TestClient

START_ENDPOINT_URL = "/chat?utterance={utterance}"
CONVERSATION_ENDPOINT_URL = "/chat?utterance={utterance}"

client = TestClient(app)

def send_prompt(prompt: str):
    start_response = client.get(START_ENDPOINT_URL.format(utterance=prompt))
    return start_response