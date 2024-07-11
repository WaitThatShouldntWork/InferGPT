import json
import logging
from src.utils import clear_scratchpad, update_scratchpad
from src.agents import get_intent_agent, get_answer_agent
from src.prompts import PromptEngine
from src.supervisors import solve_all
from src.utils import Config
from src.agents.web_agent import WebAgent

logger = logging.getLogger(__name__)
config = Config()
engine = PromptEngine()
director_prompt = engine.load_prompt("director")

# Create an instance of the WebAgent
web_agent = WebAgent(config.web_agent_llm, config.web_agent_model)

def question(question: str) -> str:
    intent = get_intent_agent().invoke(question)
    intent_json = json.loads(intent)
    logger.info(f"Intent determined: {intent}")

    try:
    # if intent_json.get('questions') and intent_json['questions'][0].get('question_category') == 'general knowledge':
    #     # Perform web search using the tool manager or handler
    #     search_results = web_agent.web_search(search_query=intent_json['query'])
    #     update_scratchpad(result=search_results)

    #     # Scrape the content from the search results
    #     scrape_results = web_agent.scrape_content(urls=search_results)
    #     update_scratchpad(result=scrape_results)

    #     # Summarise the scraped content
    #     summarisation = web_agent.summarise_content(search_query=intent_json['query'], contents=scrape_results,
    #       llm=config.web_agent_llm, model=config.web_agent_model)
    #     update_scratchpad(result=summarisation)
    #     logger.info(f"Summarisation: {summarisation}")
    # else:
        solve_all(intent_json)
    except Exception as error:
        logger.error(f"Error during task solving: {error}")
        update_scratchpad(error=str(error))

    final_answer = get_answer_agent().invoke(question)
    logger.info(f"final answer: {final_answer}")

    clear_scratchpad()

    return final_answer
