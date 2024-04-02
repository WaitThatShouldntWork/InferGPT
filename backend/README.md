# Backend

Python service for the InferGPT backend.

### Subdirectories
- `/supervisors` storing all supervisor modules (agents that call other agents for a greater goal)
- `/agents` containing all agents the director can call. Agents have their own functions stored within the agent module
- `/utils` with all shared utility modules
- `/tools` for all shared function modules

### Set up
- To install all project dependencies (listed in `requirements.txt`) run `pip install -r requirements.txt`.
- Once all dependencies have been pulled run `uvicorn api:app --port 8250` to start the app. 
- Check the backend app is running at [http://127.0.0.1:8250/health](http://127.0.0.1:8250/health).
