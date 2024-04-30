import logging
import logging.config
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import Config, test_connection
from director import question

# TODO: Add back in api_test .py from PR #37

config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.ini"))
logging.config.fileConfig(fname=config_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()
config = Config()

origins = [config.frontend_url]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

health_prefix = "InferGPT healthcheck: "
further_guidance = "Please check the README files for further guidance."

healthy_response = health_prefix + "backend is healthy. Neo4J is healthy."
unhealthy_backend_response = health_prefix + "backend is unhealthy. Unable to healthcheck Neo4J. " + further_guidance
unhealthy_neo4j_response = health_prefix + "backend is healthy. Neo4J is unhealthy. " + further_guidance

chat_fail_response = "Unable to generate a response. Check the service by using the keyphrase 'healthcheck'"

@app.get("/health")
async def health_check():
    logger.info("health_check method called")
    response = JSONResponse(status_code=200, content=healthy_response)
    try:
        if not test_connection():
            logging.info("health_check method failed - neo4j connection unsuccessful")
            response = JSONResponse(status_code=500, content=unhealthy_neo4j_response)
    except Exception as e:
        logger.critical("health_check method failed with error: " + e)
        response = JSONResponse(status_code=500, content=unhealthy_neo4j_response)
    finally:
        logging.info("health_check method complete")
        return response

@app.get("/chat")
async def chat(utterance: str):
    logger.info(f"chat method called with utterance: {utterance}")
    try:
        final_result = question(utterance)
        return JSONResponse(status_code=200, content=final_result)
    except Exception as e:
        logger.exception(e)
        return JSONResponse(status_code=500, content=chat_fail_response)
