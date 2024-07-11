import logging
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from src.prompts import PromptEngine
from src.utils import to_json
from src.utils import Config


logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()

def web_search(search_query) -> list:
    urls = []
    try:
        for url in search(search_query, num_results=5):
            urls.append(url)
    except Exception as e:
        logger.error(f"Error during web search: {e}")
    return urls


def scrape_content(urls, limit=1000) -> list:
    logger.info(f"Scraping content from URLs: {urls}")
    contents = []
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            content = ' '.join([para.get_text() for para in paragraphs])
            contents.append(content[:limit])
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            contents.append(f"Error scraping {url}: {e}")
    return contents
