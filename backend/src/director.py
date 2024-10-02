import json
import logging
from src.utils import clear_scratchpad, update_scratchpad, get_scratchpad
from src.agents import get_intent_agent, get_answer_agent
from src.prompts import PromptEngine
from src.supervisors import solve_all
from src.utils import Config
from src.websockets.connection_manager import connection_manager
from src.agents.file_agent import write_file_core

logger = logging.getLogger(__name__)
config = Config()
engine = PromptEngine()
director_prompt = engine.load_prompt("director")

conversation = []

async def get_conversation_history(user_message:str, system_message:str):
    messages = [
        {"role": "user", "content": user_message},
        {"role": "system", "content": system_message}
    ]
    conversation.append(messages)
    conversation_history = str(conversation)
    file_path = "conversation_history.txt"
    await write_file_core(file_path, conversation_history)

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
            return ""

    final_answer = await get_answer_agent().invoke(question)
    logger.info(f"final answer: {final_answer}")

    clear_scratchpad()
    await get_conversation_history(question, final_answer)

    return final_answer
