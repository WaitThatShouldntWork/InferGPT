from src.utils import call_model
from src.utils.graph_db_utils import execute_query
from src.agents import Agent, agent_metadata
import logging
from src.prompts import PromptEngine
from datetime import datetime
from src.utils import to_json
from .tool import tool_metadata
from .types import Parameter

logger = logging.getLogger(__name__)

current_user = "John Doe"
engine = PromptEngine()
narrative_options = "Bills, Groceries, Entertainment, Rent, Shopping"

graph_schema_prompt = engine.load_prompt("graph-schema", narrative_options=narrative_options)

generate_cypher_query_prompt = engine.load_prompt("generate-cypher-query",
                                                  graph_schema_prompt=graph_schema_prompt,
                                                  current_date=datetime.now())

@tool_metadata(
    name="generate cypher query",
    description="Generate Cypher query based on user utterance",
    parameters={"user_prompt": Parameter(
            type="string",
            description="Merchant name eg. Spotify",
        )
    },
)
def get_month_data(merchant_name: str) -> str:
    if merchant_name.__contains__("Amazon"):
        return "Last month you spend £64.21 on Amazon"
    if merchant_name.__contains__("Netflix"):
        return "Last month you spend £6.99 on Netflix"
    return f"Last month you didn't spend anything on {merchant_name}"


@agent_metadata(
    name="DatastoreAgent",
    description="This agent is responsible for handling database queries.",
    tools=[get_month_data],
)
class DatastoreAgent(Agent):
    pass
