import logging
from src.prompts import PromptEngine
from .agent import Agent, agent
from .tool import tool
from .agent_types import Parameter
from io import BytesIO
import base64
from src.utils import scratchpad
from PIL import Image

logger = logging.getLogger(__name__)

engine = PromptEngine()



<<<<<<< HEAD
async def generate_chart(question_intent, data_provided, question_params, llm, model) -> str:
=======

@tool(
    name="generate chart code",
    description="Generate Matplotlib bar chart code if the user's query involves creating a chart",
    parameters={
        "question_intent": Parameter(
            type="string",
            description="The intent the question will be based on",
        ),
        "categorical_values": Parameter(
            type="string",
            description="The categorical values the chart needs to represent",
        ),
        "question_params": Parameter(
            type="string",
            description="""
                The specific parameters required for the question to be answered with the question_intent
                or none if no params required
            """,
        ),
        "timeframe": Parameter(
            type="string",
            description="string of the timeframe to be considered or none if no timeframe is needed",
        ),
    },
)
def generate_chart(question_intent, categorical_values, question_params, timeframe, llm, model) -> str:
>>>>>>> b3deed22 (Correct Chart Generator Agent Name)
    details_to_generate_chart_code = engine.load_prompt(
        "details-to-generate-chart-code",
        question_intent=question_intent,
        data_provided=data_provided,
        question_params=question_params,
<<<<<<< HEAD
        scratchpad=scratchpad,
=======
        timeframe=timeframe,
>>>>>>> b3deed22 (Correct Chart Generator Agent Name)
    )

    generate_chart_code_prompt = engine.load_prompt("generate-chart-code")
    generated_code = await llm.chat(model, generate_chart_code_prompt, details_to_generate_chart_code)
    sanitised_script = sanitise_script(generated_code)
    logger.info(f"Sanitised script: {sanitised_script}")

    try:
        local_vars = {}
        exec(sanitised_script, {}, local_vars)
        fig = local_vars.get('fig')
        buf = BytesIO()
        if fig is None:
            raise ValueError("The generated code did not produce a figure named 'fig'.")
        fig.savefig(buf, format='png')
        buf.seek(0)
        with Image.open(buf):
            image_data = base64.b64encode(buf.getvalue()).decode("utf-8")

        buf.close()
    except Exception as e:
        logger.error(f"Error during chart generation or saving: {e}")
        raise
    return image_data


<<<<<<< HEAD
def sanitise_script(script: str) -> str:
    script = script.strip()
=======
def sanitise_script(script):
>>>>>>> b3deed22 (Correct Chart Generator Agent Name)
    if script.startswith("```python"):
        script = script[9:]
    if script.endswith("```"):
        script = script[:-3]
    return script.strip()

<<<<<<< HEAD
@tool(
    name="generate_code_chart",
    description="Generate Matplotlib bar chart code if the user's query involves creating a chart",
    parameters={
        "question_intent": Parameter(
            type="string",
            description="This represents the overall intent the question is attempting to answer",
        ),
        "data_provided": Parameter(
            type="string",
            description="This is the data collected to answer the user_intent. The data is stored in the scratchpad",
        ),
        "question_params": Parameter(
            type="string",
            description="""
                The specific parameters required for the question to be answered with the question_intent,
                extracted from data_provided
            """),
    }
)

async def generate_code_chart(question_intent, data_provided, question_params, llm, model) -> str:
    return await generate_chart(question_intent, data_provided, question_params, llm, model)

@agent(
    name="ChartGeneratorAgent",
    description="This agent is responsible for creating charts",
    tools=[generate_code_chart]
    tools=[generate_chart_code]
)
class CharGeneratorAgent(Agent):
    pass

