from fastapi import FastAPI
from fastapi.responses import JSONResponse
from director import question
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8650",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"message": "Infer GPT is running!"}

@app.get("/chat")
async def chat(utterance: str):
    try:
        return JSONResponse(status_code=200, content=question(utterance))
    except:
        return JSONResponse(status_code=500, content="Unable to formulate InferGPT response")
