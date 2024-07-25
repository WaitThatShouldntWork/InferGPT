from src.api import app
from fastapi.testclient import TestClient
from langchain.evaluation import load_evaluator
from langchain.evaluation import EvaluatorType
from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor

START_ENDPOINT_URL = "/chat?utterance={utterance}"
CONVERSATION_ENDPOINT_URL = "/chat?utterance={utterance}"
HEALTHCHECK_ENDPOINT_URL = "/health"
health_prefix = "InferGPT healthcheck: "
healthy_response = health_prefix + "backend is healthy. Neo4J is healthy."

client = TestClient(app)

def app_healthcheck():
    healthcheck_response = client.get(HEALTHCHECK_ENDPOINT_URL)
    return healthcheck_response

def send_prompt(prompt: str):
    start_response = client.get(START_ENDPOINT_URL.format(utterance=prompt))
    return start_response

#Evaluators
##Evaluation LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, max_retries=2)

correctness_evaluator = load_evaluator(EvaluatorType.LABELED_CRITERIA, criteria="correctness", llm=llm)

confidence_criterion = {
    "confidence": "Does the bot seem confident that it replied to the question and gave the correct answer?"
}

confidence_evaluator: load_evaluator(  # type: ignore
    EvaluatorType.CRITERIA, criteria=confidence_criterion, llm=llm
)
