import os
from dotenv import load_dotenv
from mistralai.client import MistralClient

load_dotenv()

endpoint = os.environ["INFER_GPT_MISTRAL_LARGE_ENDPOINT"]
api_key = os.environ["INFER_GPT_MISTRAL_LARGE_KEY"]
model = "azureai"

client = MistralClient(api_key=api_key,
                       endpoint=endpoint)
