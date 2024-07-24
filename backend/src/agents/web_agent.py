import logging
from src.prompts import PromptEngine
from .agent_types import Parameter
from .agent import Agent, agent
from .tool import tool
from src.utils import Config
from src.utils.web_utils import search_urls, scrape_content, summarise_content
from .validator_agent import ValidatorAgent
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()


def web_general_search_core(search_query, llm, model) -> str:
    try:
        search_result = perform_search(search_query, num_results=15)
        if search_result["status"] == "error":
            return "No relevant information found on the internet for the given query."
        urls = search_result["urls"]
        logger.info(f"URLs found: {urls}")
        for url in urls:
            content = perform_scrape(url)
            if not content:
                continue
            summary = perform_summarization(search_query, content, llm, model)
            if not summary:
                continue
            if is_valid_answer(summary, search_query):
                return summary
        return "No relevant information found on the internet for the given query."
    except Exception as e:
        logger.error(f"Error in web_general_search_core: {e}")
        return "An error occurred while processing the search query."

@tool(
    name="web_general_search",
    description="Search the internet based on the query provided and then "
                "get the meaningful answer from the content found",
    parameters={
        "search_query": Parameter(
            type="string",
            description="The search query to find information on the internet",
        ),
    },
)
def web_general_search(search_query, llm, model) -> str:
    return web_general_search_core(search_query, llm, model)

def get_validator_agent() -> Agent:
    return ValidatorAgent(config.validator_agent_llm, config.validator_agent_model)

def is_valid_answer(answer, task) -> bool:
    is_valid = (get_validator_agent().invoke(f"Task: {task}  Answer: {answer}")).lower() == "true"
    return is_valid

def perform_search(search_query: str, num_results: int) -> Dict[str, Any]:
    try:
        search_result_json = search_urls(search_query, num_results=num_results)
        return json.loads(search_result_json)
    except Exception as e:
        logger.error(f"Error during web search: {e}")
        return {"status": "error", "urls": []}

def perform_scrape(url: str) -> str:
    try:
        scrape_result_json = scrape_content(url)
        scrape_result = json.loads(scrape_result_json)
        if scrape_result["status"] == "error":
            return ""
        return scrape_result["content"]
    except Exception as e:
        logger.error(f"Error scraping content from {url}: {e}")
        return ""

def perform_summarization(search_query: str, content: str, llm: Any, model: str) -> str:
    try:
        summarise_result_json = summarise_content(search_query, content, llm, model)
        summarise_result = json.loads(summarise_result_json)
        if summarise_result["status"] == "error":
            return ""
        return summarise_result["response"]
    except Exception as e:
        logger.error(f"Error summarizing content: {e}")
        return ""

@agent(
    name="WebAgent",
    description="This agent is responsible for handling web search queries and summarizing information from the web.",
    tools=[web_general_search],
)
class WebAgent(Agent):
    pass
