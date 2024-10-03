import logging
from src.prompts import PromptEngine
from .agent_types import Parameter
from .agent import Agent, agent
from .tool import tool
from src.utils import Config
from src.utils.web_utils import (
    search_urls,
    scrape_content,
    summarise_content,
    summarise_pdf_content,
    find_info,
    create_search_term
)
from .validator_agent import ValidatorAgent
import aiohttp
import io
from pypdf import PdfReader
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()


async def web_general_search_core(search_query, llm, model) -> str:
    try:
        # Step 1: Generate the search term from the user's query
        search_term_json = await create_search_term(search_query, llm, model)
        search_term_result = json.loads(search_term_json)

        # Check if there was an error in generating the search term
        if search_term_result.get("status") == "error":
            return "No search term found for the given query."
        search_term = json.loads(search_term_result["response"]).get("search_term", "")

        # Step 2: Perform the search using the generated search term
        search_result = await perform_search(search_term, num_results=15)
        if search_result.get("status") == "error":
            return "No relevant information found on the internet for the given query."
        urls = search_result.get("urls", [])
        logger.info(f"URLs found: {urls}")

        # Step 3: Scrape content from the URLs found
        for url in urls:
            content = await perform_scrape(url)
            if not content:
                continue  # Skip to the next URL if no content is found
            logger.info(f"Content scraped successfully: {content}")
            # Step 4: Summarize the scraped content based on the search term
            summary = await perform_summarization(search_term, content, llm, model)
            if not summary:
                continue  # Skip if no summary was generated

            # Step 5: Validate the summarization
            is_valid = await is_valid_answer(summary, search_term)
            if not is_valid:
                continue # Skip if the summarization is not valid
            response = {
                "content": summary,
                "ignore_validation": "false"
            }
            return json.dumps(response, indent=4)
        return "No relevant information found on the internet for the given query."
    except Exception as e:
        logger.error(f"Error in web_general_search_core: {e}")
        return "An error occurred while processing the search query."


async def web_pdf_download_core(pdf_url, llm, model) -> str:
    try:
        async with aiohttp.request("GET", url=pdf_url) as response:
            content = await response.read()
            on_fly_mem_obj = io.BytesIO(content)
            pdf_file = PdfReader(on_fly_mem_obj)
            all_content = ""
            for page_num in range(len(pdf_file.pages)):
                page_text = pdf_file.pages[page_num].extract_text()
                summary = await perform_pdf_summarization(page_text, llm, model)
                if not summary:
                    continue
                parsed_json = json.loads(summary)
                summary = parsed_json.get('summary', '')
                all_content += summary
                all_content += "\n"
            logger.info('PDF content extracted successfully')
            response = {
                "content": all_content,
                "ignore_validation": "true"
            }
        return json.dumps(response, indent=4)
    except Exception as e:
        logger.error(f"Error in web_pdf_download_core: {e}")
        return "An error occurred while processing the search query."

@tool(
    name="web_general_search",
    description=(
        "Search the internet based on the query provided and then get the meaningful answer from the content found"
    ),
    parameters={
        "search_query": Parameter(
            type="string",
            description="The search query to find information on the internet",
        ),
    },
)
async def web_general_search(search_query, llm, model) -> str:
    return await web_general_search_core(search_query, llm, model)

@tool(
    name="web_pdf_download",
    description=(
        "Download the data from the provided pdf url"
    ),
    parameters={
        "pdf_url": Parameter(
            type="string",
            description="The pdf url to find information on the internet",
        ),
    },
)
async def web_pdf_download(pdf_url, llm, model) -> str:
    return await web_pdf_download_core(pdf_url, llm, model)

async def web_scrape_core(url: str) -> str:
    try:
        logger.info(f"Scraping the price of the book from URL: {url}")
        # Scrape the content from the provided URL
        content = await perform_scrape(url)
        if not content:
            return "No content found at the provided URL."
        logger.info(f"Content scraped successfully: {content}")
        content = content.replace("\n", " ").replace("\r", " ")
        response = {
                "content": content,
                "ignore_validation": "true"
            }
        return json.dumps(response, indent=4)
    except Exception as e:
        logger.error(f"Error in web_scrape_price_core: {e}")
        return json.dumps({"status": "error", "error": str(e)})


@tool(
    name="web_scrape",
    description="Scrapes the content from the given URL.",
    parameters={
        "url": Parameter(
            type="string",
            description="The URL of the page to scrape the content from.",
        ),
    },
)
async def web_scrape(url: str, llm, model) -> str:
    logger.info(f"Scraping the content from URL: {url}")
    return await web_scrape_core(url)


async def find_information_from_content_core(content: str, question, llm, model) -> str:
    try:
        find_info_json = await find_info(content, question, llm, model)
        info_result = json.loads(find_info_json)
        if info_result["status"] == "error":
            return ""
        final_info = info_result["response"]
        if not final_info:
            return "No information found from the content."
        logger.info(f"Content scraped successfully: {content}")
        response = {
                "content": final_info,
                "ignore_validation": "true"
            }
        return json.dumps(response, indent=4)
    except Exception as e:
        logger.error(f"Error finding information: {e}")
        return ""

@tool(
    name="find_information_content",
    description="Finds the information from the content.",
    parameters={
        "content": Parameter(
            type="string",
            description="The content to find the information from.",
        ),
        "question": Parameter(
            type="string",
            description="The question to find the information from the content.",
        ),
        },
)
async def find_information_from_content(content: str, question: str, llm, model) -> str:
    return await find_information_from_content_core(content, question, llm, model)

def get_validator_agent() -> Agent:
    return ValidatorAgent(config.validator_agent_llm, config.validator_agent_model)


async def is_valid_answer(answer, task) -> bool:
    is_valid = (await get_validator_agent().invoke(f"Task: {task}  Answer: {answer}")).lower() == "true"
    return is_valid


async def perform_search(search_query: str, num_results: int) -> Dict[str, Any]:
    try:
        search_result_json = await search_urls(search_query, num_results=num_results)
        return json.loads(search_result_json)
    except Exception as e:
        logger.error(f"Error during web search: {e}")
        return {"status": "error", "urls": []}


async def perform_scrape(url: str) -> str:
    try:
        scrape_result_json = await scrape_content(url)
        scrape_result = json.loads(scrape_result_json)
        if scrape_result["status"] == "error":
            return ""
        return scrape_result["content"]
    except Exception as e:
        logger.error(f"Error scraping content from {url}: {e}")
        return ""


async def perform_summarization(search_query: str, content: str, llm: Any, model: str) -> str:
    try:
        summarise_result_json = await summarise_content(search_query, content, llm, model)
        summarise_result = json.loads(summarise_result_json)
        if summarise_result["status"] == "error":
            return ""
        logger.info(f"Content summarized successfully: {summarise_result['response']}")
        return json.loads(summarise_result["response"])["summary"]
    except Exception as e:
        logger.error(f"Error summarizing content: {e}")
        return ""

async def perform_pdf_summarization(content: str, llm: Any, model: str) -> str:
    try:
        summarise_result_json = await summarise_pdf_content(content, llm, model)
        summarise_result = json.loads(summarise_result_json)
        if summarise_result["status"] == "error":
            return ""
        return summarise_result["response"]
    except Exception as e:
        logger.error(f"Error summarizing content: {e}")
        return ""

@agent(
    name="WebAgent",
    description="""This agent specializes in handling tasks related to web content extraction, search, and
    summarization.
    It can perform the following functions:
    Web scraping: Extracts data from given URLs, enabling tasks like retrieving specific information from web pages.
    Finding Information from Content: Extracts specific information from the content provided.
    Internet search: Conducts general online searches based on queries, retrieving and summarizing relevant content from
    multiple sources.
    PDF content extraction: Downloads and summarizes the content of PDF documents from provided URLs.""",
    tools=[web_general_search, web_pdf_download, web_scrape, find_information_from_content],
)
class WebAgent(Agent):
    pass
