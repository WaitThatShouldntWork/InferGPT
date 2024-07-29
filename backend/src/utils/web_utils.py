import logging
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from src.prompts import PromptEngine
from src.utils import Config
import json


logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()


def search_urls(search_query, num_results=10) -> str:
    logger.info(f"Searching the web for: {search_query}")
    urls = []
    try:
        for url in search(search_query, num_results=num_results):
            urls.append(url)
        return json.dumps({"status": "success", "urls": urls, "error": None})
    except Exception as e:
        logger.error(f"Error during web search: {e}")
        return json.dumps({"status": "error", "urls": [], "error": str(e)})


def scrape_content(url, limit=100000) -> str:
    try:
        logger.info(f"Scraping content from URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = " ".join([para.get_text() for para in paragraphs])
        return json.dumps({"status": "success", "content": content[:limit], "error": None})
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return json.dumps({"status": "error", "content": "", "error": str(e)})


def summarise_content(search_query, contents, llm, model) -> str:
    try:
        summariser_prompt = engine.load_prompt("summariser", question=search_query, content=contents)
        response = llm.chat(model, summariser_prompt, "", return_json=True)
        return json.dumps({"status": "success", "response": response, "error": None})
    except Exception as e:
        logger.error(f"Error during summarisation: {e}")
        return json.dumps({"status": "error", "response": None, "error": str(e)})
