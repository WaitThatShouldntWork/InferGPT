import logging
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from src.prompts import PromptEngine
from datetime import datetime
from src.utils import to_json
from .agent_types import Parameter
from .agent import Agent, agent
from .tool import tool
from src.utils import Config


logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()

@tool(
    name="web_search",
    description="Search the internet based on the query provided",
    parameters={
        "search_query": Parameter(
            type="string",
            description="The search query to find information on the internet",
        ),
    },
)
def web_search(search_query, llm, model) -> list:
    urls = []
    try:
        for url in search(search_query, num_results=1):
            urls.append(url)
    except Exception as e:
        logger.error(f"Error during web search: {e}")
    # return urls
    logger.info(f"############# URLs found: {urls}")
    contents = []
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            content = ' '.join([para.get_text() for para in paragraphs])
            contents.append(content[:500])
            logger.info(f"Scraped content from {url}- {content[:500]}")
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            contents.append(f"Error scraping {url}: {e}")

    combined_content = "\n\n".join([f"{i+1}. {content}" for i, content in enumerate(contents)])
    prompt = (
        f"User Query: {search_query}\n\n"
        f"You are an experienced document reader. Based on the user's query, read through the content provided below "
        f"and answer the query.\n\n"
        f"Contents:\n{combined_content}"
    )
    response = llm.chat(model, prompt, "")
    logger.info(f"############# Response from LLM: {response}")
    return response

@tool(
    name="scrape_content",
    description="Scrape content from the given URLs",
    parameters={
        "urls": Parameter(
            type="list",
            description="The list of URLs to scrape content from",
        ),
    },
)
def scrape_content(urls) -> list:
    logger.info(f"Scraping content from URLs: {urls}")
    contents = []
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            content = ' '.join([para.get_text() for para in paragraphs])
            contents.append(content)
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            contents.append(f"Error scraping {url}: {e}")
    return contents

@tool(
    name="summarize_content",
    description="Summarize the scraped content to answer the user's query",
    parameters={
        "search_query": Parameter(
            type="string",
            description="The original search query from the user",
        ),
        "contents": Parameter(
            type="list",
            description="The list of contents scraped from the URLs",
        ),
    },
)
def summarize_content(search_query, contents, llm, model) -> str:
    combined_content = "\n\n".join([f"{i+1}. {content}" for i, content in enumerate(contents)])
    prompt = (
        f"User Query: {search_query}\n\n"
        f"You are an experienced document reader. Based on the user's query, read through the content provided below "
        f"and answer the query.\n\n"
        f"Contents:\n{combined_content}"
    )
    response = llm.chat(model, prompt, "")
    return response

@agent(
    name="WebAgent",
    description="This agent is responsible for handling web search queries and summarizing information from the web.",
    tools=[web_search, scrape_content, summarize_content],
)
class WebAgent(Agent):
    pass
