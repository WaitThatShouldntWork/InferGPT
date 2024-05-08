from .tool import tool_metadata
from .types import Parameter
from src.agents import Agent, agent_metadata


@tool_metadata(
    name="last month data",
    description="Get spending for the last month on a merchant",
    parameters={
        "merchant_name": Parameter(
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
