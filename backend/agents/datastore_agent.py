from .tool import tool_metadata
from .types import Parameter
from agents import Agent, agent_metadata


@tool_metadata(
    name="last month data",
    description="Get spending for the last month on a merchant",
    parameters={
        "merchant": Parameter(
            type="string",
            description="Merchant name eg. Spotify",
        )
    },
)
def get_month_data(merchant: str) -> str:
    if merchant.__contains__("Amazon"):
        return "Last month you spend £64.21 on Amazon"
    elif merchant.__contains__("Netflix"):
        return "Last month you spend £6.99 on Netflix"
    else:
        return "Last month you didn't spend anything on " + merchant

data_store_prompt = """
You are an expert database agent. You can help with database queries and are connected to a neo4j database.

When looking for an input to any tool being used, a single mechant should be provided.

e.g. "Calculate the sum of Netflix spend over the last month"
Merchant: Netflix
"""


@agent_metadata(
    name="DatastoreAgent",
    description="This agent is responsible for handling database queries.",
    prompt=data_store_prompt,
    tools=[get_month_data],
)
class DatastoreAgent(Agent):
    pass
