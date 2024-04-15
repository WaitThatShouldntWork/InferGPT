import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import Config
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


@app.get("/health")
async def health_check():
    logger.info("health_check method called successfully")
    return {"message": "InferGPT backend is healthy"}


@app.get("/chat")
async def chat(utterance: str):
    logger.info(f"chat method called with utterance: {utterance}")
    try:
        return JSONResponse(status_code=200, content=question(utterance))
    except Exception as e:
        logger.exception(e)
        return JSONResponse(
            status_code=500, content="Unable to formulate InferGPT response"
        )
