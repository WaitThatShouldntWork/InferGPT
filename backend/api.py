# TODO: Add basic FastAPI app for communicating with the front end

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"message": "Infer GPT is running!"}
