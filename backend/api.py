# TODO: Add basic FastAPI app for communicating with the front end

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
