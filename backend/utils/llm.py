import os
from dotenv import load_dotenv
from mistralai.client import MistralClient

load_dotenv()

endpoint = os.environ["AZURE_AI_MISTRAL_LARGE_ENDPOINT"]
api_key = os.environ["AZURE_AI_MISTRAL_LARGE_KEY"]
model = "azureai"

client = MistralClient(api_key=api_key,
                       endpoint=endpoint)
