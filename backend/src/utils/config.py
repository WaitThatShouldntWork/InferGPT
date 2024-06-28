import os
from dotenv import load_dotenv

default_frontend_url = "http://localhost:8650"
default_neo4j_uri = "bolt://localhost:7687"


class Config(object):
    def __init__(self):
        self.frontend_url = default_frontend_url
        self.mistral_url = None
        self.mistral_key = None
        self.mistral_model = None
        self.openai_key = None
        self.openai_model = None
        self.neo4j_uri = default_neo4j_uri
        self.neo4j_user = None
        self.neo4j_password = None
        self.azure_storage_connection_string = None
        self.azure_storage_container_name = None
        self.azure_initial_data_filename = None
        self.answer_agent_llm = None
        self.intent_agent_llm = None
        self.validator_agent_llm = None
        self.datastore_agent_llm = None
        self.maths_agent_llm = None
        self.router_llm = None
        self.answer_agent_model = None
        self.intent_agent_model = None
        self.validator_agent_model = None
        self.datastore_agent_model = None
        self.maths_agent_model = None
        self.router_model = None
        self.load_env()

    def load_env(self):
        """
        Load environment variables from .env file.
        """
        load_dotenv()
        try:
            self.frontend_url = os.getenv("FRONTEND_URL", default_frontend_url)
            self.mistral_url = os.getenv("MISTRAL_URL")
            self.mistral_key = os.getenv("MISTRAL_KEY")
            self.mistral_model = os.getenv("MODEL")
            self.openai_key = os.getenv("OPENAI_KEY")
            self.openai_model = os.getenv("OPENAI_MODEL")
            self.neo4j_uri = os.getenv("NEO4J_URI", default_neo4j_uri)
            self.neo4j_user = os.getenv("NEO4J_USERNAME")
            self.neo4j_password = os.getenv("NEO4J_PASSWORD")
            self.azure_storage_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            self.azure_storage_container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
            self.azure_initial_data_filename = os.getenv("AZURE_INITIAL_DATA_FILENAME")
            self.answer_agent_llm = os.getenv("ANSWER_AGENT_LLM")
            self.intent_agent_llm = os.getenv("INTENT_AGENT_LLM")
            self.validator_agent_llm = os.getenv("VALIDATOR_AGENT_LLM")
            self.datastore_agent_llm = os.getenv("DATASTORE_AGENT_LLM")
            self.maths_agent_llm = os.getenv("MATHS_AGENT_LLM")
            self.router_llm = os.getenv("ROUTER_LLM")
            self.answer_agent_model = os.getenv("ANSWER_AGENT_MODEL")
            self.intent_agent_model = os.getenv("INTENT_AGENT_MODEL")
            self.validator_agent_model = os.getenv("VALIDATOR_AGENT_MODEL")
            self.datastore_agent_model = os.getenv("DATASTORE_AGENT_MODEL")
            self.maths_agent_model = os.getenv("MATHS_AGENT_MODEL")
            self.router_model = os.getenv("ROUTER_MODEL")
        except FileNotFoundError:
            raise FileNotFoundError("Please provide a .env file. See the Getting Started guide on the README.md")
        except Exception:
            raise Exception("Missing .env file property. See the Getting Started guide on the README.md")
