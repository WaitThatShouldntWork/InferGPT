from .tool import tool_metadata
from .types import Parameter
from agents import Agent, agent_metadata


@tool_metadata(
    name="Get Database Data",
    description="This tool gets data from the database",
    parameters={
        "merchant": Parameter(
            type="string",
            description="Merchant name eg. Amazon",
        )
    },
)
def get_db_data(merchant: str) -> str:
    print(f"Getting data from database with merchant: {merchant}")
    return "6.99"


data_store_prompt = """
You are an expert database agent. You can help with database queries and are connected to a neo4j database.

When looking for an input to any tool being used, a single mechant should be provided.

e.g. "Calculate the sum of Netflix spend over the last month"
Merchant: Netflix
"""


@agent_metadata(
    name="DatastoreAgent",
    description="This agent is responsible for handling database queries. It is best at finding personal data on the user",
    prompt=data_store_prompt,
    tools=[get_db_data],
)
class DatastoreAgent(Agent):
    pass
