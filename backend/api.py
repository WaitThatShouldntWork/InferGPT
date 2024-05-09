import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from utils import test_connection
from utils import Config
from director import question
from fastapi.middleware.cors import CORSMiddleware

logging.config.fileConfig(fname='config.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()
config = Config()

origins = [ config.frontend_url ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    try:
        logger.info("health_check method called successfully")
        neo4j_status = "healthy" if test_connection() == True else "unhealthy. Please check the README files for further guidance"
        logging.info("health_check method complete")
        return JSONResponse(status_code=200, content="InferGPT healthcheck: backend is healthy. Neo4J is " + neo4j_status)
    except Exception as e:
        logger.critical("health_check method failed with error: " + e)
        return JSONResponse(status_code=500, content="InferGPT healthcheck: backend is unhealthy. Unable to healthcheck Neo4J. Please check the README files for further guidance")

@app.get("/chat")
async def chat(utterance: str):
    logger.info("chat method called with utterance \"{0}\"".format(utterance))
    try:
        return JSONResponse(status_code=200, content=question(utterance))
    except Exception as e:
        logger.exception(e)
        return JSONResponse(status_code=500, content="Unable to generate InferGPT response")
