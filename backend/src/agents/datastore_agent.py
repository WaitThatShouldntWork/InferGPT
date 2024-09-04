import json
import logging
from src.llm.llm import LLM
from src.utils.graph_db_utils import execute_query
from src.prompts import PromptEngine
from datetime import datetime
from src.utils import to_json
from .agent_types import Parameter
from src.utils.log_publisher import LogPrefix, publish_log_info
from .agent import Agent, agent
from .tool import tool
from src.utils.semantic_layer_builder import get_semantic_layer

logger = logging.getLogger(__name__)

engine = PromptEngine()

cache = {}

async def generate_cypher_query_core(
    question_intent, operation, question_params, aggregation, sort_order, timeframe, llm: LLM, model
) -> str:

    async def get_semantic_layer_cache(graph_schema):
        global cache
        if not cache:
            graph_schema = await get_semantic_layer(llm, model)
            cache = graph_schema
            return cache
        else:
            return cache

    details_to_create_cypher_query = engine.load_prompt(
        "details-to-create-cypher-query",
        question_intent=question_intent,
        operation=operation,
        question_params=question_params,
        aggregation=aggregation,
        sort_order=sort_order,
        timeframe=timeframe,
    )
    try:
        graph_schema = await get_semantic_layer_cache(cache)
        graph_schema = json.dumps(graph_schema, separators=(",", ":"))

        generate_cypher_query_prompt = engine.load_prompt(
            "generate-cypher-query", graph_schema=graph_schema, current_date=datetime.now()
        )

        llm_query = await llm.chat(model, generate_cypher_query_prompt, details_to_create_cypher_query,
                                   return_json=True)
        json_query = to_json(llm_query)
        await publish_log_info(LogPrefix.USER, f"Cypher generated by the LLM: {llm_query}", __name__)
        if json_query["query"] == "None":
            return "No database query"
        db_response = execute_query(json_query["query"])
        await publish_log_info(LogPrefix.USER, f"Database response: {db_response}", __name__)
    except Exception as e:
        logger.error(f"Error during data retrieval: {e}")
        raise
    return str(db_response)

@tool(
    name="generate cypher query",
    description="Generate Cypher query if the category is data driven, based on the operation to be performed",
    parameters={
        "question_intent": Parameter(
            type="string",
            description="The intent the question will be based on",
        ),
        "operation": Parameter(
            type="string",
            description="The operation the cypher query will have to perform",
        ),
        "question_params": Parameter(
            type="string",
            description="""
                The specific parameters required for the question to be answered with the question_intent
                or none if no params required
            """,
        ),
        "aggregation": Parameter(
            type="string",
            description="Any aggregation that is required to answer the question or none if no aggregation is needed",
        ),
        "sort_order": Parameter(
            type="string",
            description="The order a list should be sorted in or none if no sort_order is needed",
        ),
        "timeframe": Parameter(
            type="string",
            description="string of the timeframe to be considered or none if no timeframe is needed",
        ),
    },
)

async def generate_cypher(question_intent, operation, question_params, aggregation, sort_order,
                          timeframe, llm: LLM, model) -> str:
    return await generate_cypher_query_core(question_intent, operation, question_params, aggregation, sort_order,
                                            timeframe, llm, model)

@agent(
    name="DatastoreAgent",
    description="This agent is responsible for handling database queries relating to the user's personal data.",
    tools=[generate_cypher],
)
class DatastoreAgent(Agent):
    pass
