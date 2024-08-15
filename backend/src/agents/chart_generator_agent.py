import logging
from src.prompts import PromptEngine
from .agent import Agent, agent
from .tool import tool
from .agent_types import Parameter
from io import BytesIO
import base64
from src.websockets.connection_manager import connection_manager
from src.utils import scratchpad
from PIL import Image

logger = logging.getLogger(__name__)

engine = PromptEngine()

def generate_chart(question_intent, categorical_values, question_params, timeframe, llm, model) -> str:
    details_to_generate_chart_code = engine.load_prompt(
        "details-to-generate-chart-code",
        question_intent=question_intent,
        data_provided=data_provided,
        question_params=question_params,
        scratchpad=scratchpad,
    )
    generate_chart_code_prompt = engine.load_prompt("generate-chart-code")
    generated_code = llm.chat(model, generate_chart_code_prompt, details_to_generate_chart_code)
    sanitised_script = sanitise_script(generated_code)
    logger.info(f"Sanitised script: {sanitised_script}")

    try:

        local_vars = {}
        exec(sanitised_script, {}, local_vars)
        fig = local_vars.get('fig')

        if fig is None:
            raise ValueError("The generated code did not produce a figure named 'fig'.")
        # buf = BytesIO()
        # saved_fig = fig.savefig(buf, format='png')
        output_dir = '/app/output'

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        logger.info("Saving the figure as 'output.png'")
        output_path = os.path.join(output_dir, "output.png")
        fig.savefig(output_path)
        logger.info(f"Figure saved successfully as {output_path}")

        with open(output_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")

        await connection_manager.send_chart({"type": "image", "data": image_data})


    except Exception as e:
        logger.error(f"Error during chart generation or saving: {e}")
        raise
    return image_data

def sanitise_script(script: str) -> str:
    script = script.strip()
    if script.startswith("```python"):
        script = script[9:]
    if script.endswith("```"):
        script = script[:-3]
    return script.strip()

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
            description="This is the data collected to answer the user_intent. The data is stored in the {scratchpad}",
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
    name="CharGeneratorAgent",
    description="This agent is responsible for creating charts",
    tools=[generate_code_chart]
)

class ChartGeneratorAgent(Agent):
    pass
