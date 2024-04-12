import os
from dotenv import load_dotenv


class Config(object):
    def __init__(self):
        self.frontend_url = None
        self.mistralruf_url = None
        self.mistralruf_key = None
        self.mistralruf_model = None
        self.neo4j_uri = None
        self.neo4j_user = None
        self.neo4j_password = None
        self.load_env()

    def load_env(self):
        """
        Load environment variables from .env file.
        """
        load_dotenv()
        try:
            self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8650")
            self.mistral_url = os.getenv("MISTRAL_URL")
            self.mistral_key = os.getenv("MISTRAL_KEY")
            self.mistral_model = os.getenv("MODEL")
            self.neo4j_uri = os.getenv("NEO4J_URI")
            self.neo4j_user = os.getenv("NEO4J_USERNAME")
            self.neo4j_password = os.getenv("NEO4J_PASSWORD")
        except FileNotFoundError:
            raise FileNotFoundError(
                "Please provide a .env file. See the Getting Started guide on the README.md"
            )
        except Exception:
            raise Exception(
                "Missing .env file property. See the Getting Started guide on the README.md"
            )
