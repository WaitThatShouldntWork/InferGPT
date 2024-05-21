from uvicorn import run
from src.api import app

run(app, port=8250)
