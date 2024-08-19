import json
import logging
from src.utils import clear_scratchpad, update_scratchpad, get_scratchpad
from src.agents import get_intent_agent, get_answer_agent
from src.prompts import PromptEngine
from src.supervisors import solve_all
from src.utils import Config
from src.websockets.connection_manager import connection_manager

logger = logging.getLogger(__name__)
config = Config()
engine = PromptEngine()
director_prompt = engine.load_prompt("director")


async def question(question: str) -> str:
    intent = await get_intent_agent().invoke(question)
    intent_json = json.loads(intent)
    logger.info(f"Intent determined: {intent}")

    try:
        await solve_all(intent_json)
    except Exception as error:
        logger.error(f"Error during task solving: {error}")
        update_scratchpad(error=str(error))

    current_scratchpad = get_scratchpad()

    for entry in current_scratchpad:
        if entry["agent_name"] == "ChartGeneratorAgent":
            generated_figure = entry["result"]
            await connection_manager.send_chart({"type": "image", "data": generated_figure})
            clear_scratchpad()


    final_answer = await get_answer_agent().invoke(question)
    logger.info(f"final answer: {final_answer}")

    clear_scratchpad()

    return final_answer

def get_result_by_agent(agent_name: str) -> str | None:
    scratchpad = get_scratchpad()

    for entry in scratchpad:
        if entry["agent_name"] == agent_name:
            return entry["result"]
    return None
