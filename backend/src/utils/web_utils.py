import logging
from googlesearch import search
import aiohttp
from bs4 import BeautifulSoup
from src.prompts import PromptEngine
from src.utils import Config
import json


logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()


async def search_urls(search_query, num_results=10) -> str:
    logger.info(f"Searching the web for: {search_query}")
    urls = []
    try:
        for url in search(search_query, num_results=num_results):
            urls.append(url)
        return json.dumps(
            {
                "status": "success",
                "urls": urls,
                "error": None,
            }
        )
    except Exception as e:
        logger.error(f"Error during web search: {e}")
        return json.dumps(
            {
                "status": "error",
                "urls": [],
                "error": str(e),
            }
        )


async def scrape_content(url, limit=100000) -> str:
    try:
        logger.info(f"Scraping content from URL: {url}")
        async with aiohttp.request("GET", url) as response:
            response.raise_for_status()
            soup = BeautifulSoup(await response.text(), "html.parser")
            paragraphs = soup.find_all("p")
            content = " ".join([para.get_text() for para in paragraphs])
            return json.dumps(
                {
                    "status": "success",
                    "content": content[:limit],
                    "error": None,
                }
            )
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return json.dumps(
            {
                "status": "error",
                "content": "",
                "error": str(e),
            }
        )


async def summarise_content(search_query, contents, llm, model) -> str:
    try:
        summariser_prompt = engine.load_prompt("summariser", question=search_query, content=contents)
        response = await llm.chat(model, summariser_prompt, "", return_json=True)
        return json.dumps(
            {
                "status": "success",
                "response": response,
                "error": None,
            }
        )
    except Exception as e:
        logger.error(f"Error during summarisation: {e}")
        return json.dumps(
            {
                "status": "error",
                "response": None,
                "error": str(e),
            }
        )

async def summarise_pdf_content(contents, llm, model) -> str:
    try:
        summariser_prompt = engine.load_prompt("pdf-summariser", content=contents)
        response = await llm.chat(model, summariser_prompt, "", return_json=True)
        return json.dumps(
            {
                "status": "success",
                "response": response,
                "error": None,
            }
        )
    except Exception as e:
        logger.error(f"Error during summarisation: {e}")
        return json.dumps(
            {
                "status": "error",
                "response": None,
                "error": str(e),
            }
        )

async def perform_math_operation_util(math_query, llm, model) -> str:
    try:
        # Load the prompt template for math operations
        math_prompt = engine.load_prompt("math-solver", query=math_query)

        # Send the math query to the LLM to perform the math operation
        response = await llm.chat(model, math_prompt, "", return_json=True)
        # Parse the response and return the result
        return json.dumps(
            {
                "status": "success",
                "response": response,  # math result
                "error": None,
            }
        )
    except Exception as e:
        # Handle any errors during the LLM math operation
        logger.error(f"Error during math operation: {e}")
        return json.dumps(
            {
                "status": "error",
                "response": None,
                "error": str(e),
            }
        )
