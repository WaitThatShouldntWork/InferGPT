
import os
import yaml

default_frontend_url = "http://localhost:8650"
default_neo4j_uri = "bolt://localhost:7687"

class Config(object):
    def __init__(self, config_path="env.yml"):
        self.frontend_url = default_frontend_url
        self.mistral_key = None
        self.openai_key = None
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
        self.web_agent_llm = None
        self.maths_agent_llm = None
        self.router_llm = None
        self.chart_generator_llm = None
        self.answer_agent_model = None
        self.intent_agent_model = None
        self.validator_agent_model = None
        self.datastore_agent_model = None
        self.web_agent_model = None
        self.maths_agent_model = None
        self.router_model = None
        self.chart_generator_model = None
        self.agent_class_model = None

        # We don't want to load the environment variables when running tests
        if os.getenv("PYTEST_RUNNING") is None:
            self.load_env(config_path)

    def load_env(self, config_path):
        """
        Load environment variables from env.yml file.
        """
        try:
            # Construct the absolute path
            config_path = os.path.join(os.getcwd(), config_path)
            with open(config_path, "r") as file:
                config = yaml.safe_load(file)
            # self.frontend_url = config.get("frontend_url", default_frontend_url)
            # self.mistral_key = config.get("mistral_key")
            # self.openai_key = config.get("openai_key")
            self.frontend_url = config.get("urls", {}).get("frontend", default_frontend_url)
            self.mistral_key = config.get("keys", {}).get("mistral")
            self.openai_key = config.get("keys", {}).get("openai")
            self.neo4j_uri = config.get("neo4j", {}).get("uri", default_neo4j_uri)
            self.neo4j_user = config.get("neo4j", {}).get("username")
            self.neo4j_password = config.get("neo4j", {}).get("password")
            self.azure_storage_connection_string = config.get("azure", {}).get("storage_connection_string")
            self.azure_storage_container_name = config.get("azure", {}).get("storage_container_name")
            self.azure_initial_data_filename = config.get("azure", {}).get("initial_data_filename")
            self.answer_agent_llm = config.get("agents", {}).get("answer", {}).get("llm")
            self.intent_agent_llm = config.get("agents", {}).get("intent", {}).get("llm")
            self.validator_agent_llm = config.get("agents", {}).get("validator", {}).get("llm")
            self.datastore_agent_llm = config.get("agents", {}).get("datastore", {}).get("llm")
            self.web_agent_llm = config.get("agents", {}).get("web", {}).get("llm")
            self.maths_agent_llm = config.get("agents", {}).get("maths", {}).get("llm")
            self.router_llm = config.get("agents", {}).get("router", {}).get("llm")
            self.answer_agent_model = config.get("agents", {}).get("answer", {}).get("model")
            self.intent_agent_model = config.get("agents", {}).get("intent", {}).get("model")
            self.validator_agent_model = config.get("agents", {}).get("validator", {}).get("model")
            self.datastore_agent_model = config.get("agents", {}).get("datastore", {}).get("model")
            self.web_agent_model = config.get("agents", {}).get("web", {}).get("model")
            self.maths_agent_model = config.get("agents", {}).get("maths", {}).get("model")
            self.router_model = config.get("agents", {}).get("router", {}).get("model")
            self.agent_class_model = config.get("agents", {}).get("agent_class", {}).get("model")
            self.chart_generator_model = config.get("agents", {}).get("agent_class", {}).get("model")

        except FileNotFoundError:
            raise FileNotFoundError("Please provide a env.yml file. See the Getting Started guide on the README.md")
        except Exception as e:
            raise Exception(f"Error loading configuration file: {e}")
