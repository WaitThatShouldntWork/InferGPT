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
from src.utils.web_utils import web_search as find_urls, scrape_content
from src.utils import clear_scratchpad, update_scratchpad


logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()

@tool(
    name="web_general_search",
    description="Search the internet based on the query provided and then get the meaningful answer from the content found",
    parameters={
        "search_query": Parameter(
            type="string",
            description="The search query to find information on the internet",
        ),
    },
)
def web_general_search(search_query, llm, model) -> list:

    urls = []
    urls = find_urls(search_query)
    logger.info(f"############# URLs found: {urls}")
    if not urls:
        return ["No relevant information found on the internet for the given query."]
    update_scratchpad(result=urls)
    contents = scrape_content(urls)
    if not contents:
        return ["No relevant information found on the internet for the given query."]
    update_scratchpad(result=contents)

    final_response = summarise_content(search_query, contents, llm, model)

    if final_response:
        update_scratchpad(result=final_response)
        return [final_response]
    else:
        return ["No relevant information found on the internet for the given query."]

# @tool(
#     name="scrape_content",
#     description="Scrape content from the given URLs",
#     parameters={
#         "urls": Parameter(
#             type="list",
#             description="The list of URLs to scrape content from",
#         ),
#     },
# )
# def scrape_content(urls) -> list:
#     logger.info(f"Scraping content from URLs: {urls}")
#     contents = []
#     for url in urls:
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, 'html.parser')
#             paragraphs = soup.find_all('p')
#             content = ' '.join([para.get_text() for para in paragraphs])
#             contents.append(content)
#         except Exception as e:
#             logger.error(f"Error scraping {url}: {e}")
#             contents.append(f"Error scraping {url}: {e}")
#     return contents

@tool(
    name="summarise_content",
    description="Summarise the scraped content to answer the user's query",
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
def summarise_content(search_query, contents, llm, model) -> str:
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
    tools=[web_general_search],
)
class WebAgent(Agent):
    pass
