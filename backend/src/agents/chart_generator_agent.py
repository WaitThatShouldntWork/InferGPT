import logging
from src.prompts import PromptEngine
from .agent import Agent, agent
from .tool import tool
from .types import Parameter

logger = logging.getLogger(__name__)

engine = PromptEngine()

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
    }
)

def generate_chart_code(question_intent, categorical_values, question_params, timeframe, llm, model) -> str:
    details_to_generate_chart_code = engine.load_prompt(
        "details-to-generate-chart-code",
        question_intent=question_intent,
        categorical_values=categorical_values,
        question_params=question_params,
        timeframe=timeframe
    )
    generate_chart_code_prompt = engine.load_prompt("generate-chart-code")
    generate_code = llm.chat(model, generate_chart_code_prompt, details_to_generate_chart_code)
    print(generate_chart_code)
    return generate_code


@agent(
    name="CharGeneratorAgent",
    description="This agent is responsible for creating charts",
    tools=[generate_chart_code]
)
class CharGeneratorAgent(Agent):
    pass
