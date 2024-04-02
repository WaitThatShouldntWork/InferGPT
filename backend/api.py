from fastapi import FastAPI
from fastapi.responses import JSONResponse
from director import question

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"message": "Infer GPT is running!"}

@app.get("/chat")
async def chat(utterance: str):
    try:
        return JSONResponse(status_code=200, content=question(utterance))
    except:
        return JSONResponse(status_code=500, content="Unable to formulate InferGPT response")
