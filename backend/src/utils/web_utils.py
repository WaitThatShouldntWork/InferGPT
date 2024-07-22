import logging
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from src.prompts import PromptEngine
from src.utils import Config


logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()

def search_urls(search_query) -> list:
    logger.info(f"Searching the web for: {search_query}")
    urls = []
    try:
        for url in search(search_query, num_results=5):
            urls.append(url)
    except Exception as e:
        logger.error(f"Error during web search: {e}")
    return urls


def scrape_content(url, limit=100000) -> list:
    try:
        logger.info(f"Scraping content from URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        return content[:limit]
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
def summarise_content(search_query, contents, llm, model) -> str:
    logger.info(f"######### combined_content ######### {contents}")
    summariser_prompt =  engine.load_prompt(
        "summariser",
        question=search_query,
        content=contents
    )

    response = llm.chat(model, summariser_prompt, "")
    return response
