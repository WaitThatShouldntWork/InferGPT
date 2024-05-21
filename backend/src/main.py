from uvicorn import run
import argparse
from src.api import app

parser = argparse.ArgumentParser(description='Run the backend server')
parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to run the server on')
args = parser.parse_args()

run(app, port=8250, host=args.host)
