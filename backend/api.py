import logging
import logging.config
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import Config, test_connection
from director import question

logging.config.fileConfig(fname="config.ini", disable_existing_loggers=False)
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

healthy_response = {"message": "InferGPT backend is healthy"}
error_message = "Unable to formulate InferGPT response"
health_prefix = "InferGPT healthcheck: "
unhealthy_neo4j_response = "unhealthy. Please check the README files for further guidance"


@app.get("/health")
async def health_check():
    try:
        logger.info("health_check method called successfully")
        neo4j_status = "healthy" if test_connection() else unhealthy_neo4j_response
        logging.info("health_check method complete")
        return JSONResponse(status_code=200, content=health_prefix + "backend is healthy. Neo4J is " + neo4j_status)
    except Exception as e:
        logger.critical("health_check method failed with error: " + e)
        return JSONResponse(status_code=500, content=health_prefix +
            "backend is unhealthy. Unable to healthcheck Neo4J. Please check the README files for further guidance"
        )

@app.get("/chat")
async def chat(utterance: str):
    logger.info(f"chat method called with utterance: {utterance}")
    try:
        return JSONResponse(status_code=200, content=question(utterance))
    except Exception as e:
        logger.exception(e)
        return JSONResponse(status_code=500, content="Unable to generate InferGPT response")
