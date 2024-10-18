# Backend

Python service for the InferGPT backend.

## Structure
- `/supervisors` storing all supervisor modules (agents that call other agents for a greater goal)
- `/agents` containing all agents the director can call. Agents have their own functions stored within the agent module
- `/utils` with all shared utility modules
- `/tools` for all shared function modules

## Set up

1. Ensure the `.env` file has been configured as described in the main [README](../README.md).

> Note: You will need to configure a LLM to run the service.

This README covers instructions on how to run the application:
- Locally
- In a Docker Container

For ease of use, we would recommended that you run the entire application using **Docker Compose** instead. See main [README](../README.md).

If you would prefer not to use **Docker Compose**, read on...

Unless otherwise stated all of the commands mentioned in this README should be run from `./backend`.

## Running Locally

Follow the instructions below to run the backend locally. Change directory to `/backend`, then follow the instructions below.

1. Set-up a virtual environment

> It's recommended (though not technically required) to create a virtual environment for the project by running `python -m venv .venv` to create it and `.venv/Scripts/activate` to activate it in your active terminal.

2. Install dependencies

```bash
pip install -r requirements.txt
```
> (VsCode) You may run into some issues with compiling python packages from requirements.txt. To resolve this ensure you have downloaded and installed the "Desktop development with C++" workload from your Visual Studio installer.
3. Run the app

```bash
uvicorn src.api:app --port 8250
```

4. Check the backend app is running at [http://localhost:8250/health](http://localhost:8250/health)

## Running in a Docker Container

1. Build the Docker image

```bash
docker build -t {my-backend-image-name} .
```

2. Run the backend within a Docker container

```bash
docker run --env-file ../.env -p 8250:8250 {my-backend-image-name}
```

> Note that we pass in the entire environment file that contains all our application's configuration. This means some unneccessary configuration is also being passed in. This is fine when testing locally. In production, we must limit this to only the essential backend configuration (see environment configuration within [Docker Compose](../compose.yml)).

3. Check the backend app is running at [http://localhost:8250/health](http://localhost:8250/health)

## Linting

Ruff is being used for the backend linting. See the docs: [here](https://docs.astral.sh/ruff/)

Make sure the ruff dependency is downloaded; It is defined in the `requirements.txt` so step `1` of [setup](#set-up) should do this for you.

Run the following command to check:

```bash
ruff --version
```

If it is not installed use the following command:

```bash
pip install ruff
```

If ruff is installed correctly, the python files in the backend will be checked using the following command, from the backend directory:

```bash
ruff check
```

You can run the following command to fix any errors automatically:

```bash
ruff format
```

The ruff vscode plugin can also be installed from the store to show linting errors in the IDE.

### Linting Rules

Currently there are 4 rule groups selected in`ruff.toml`. All rule groups can be found [here](https://docs.astral.sh/ruff/rules/).

To add further rules, these are added to `ruff.toml` by using the letter asssigned to the rules as in the docs linked above. ie. pep8-naming uses the letter "N".

## Test

`pytest` is being used for testing the backend. Like with linting, running the [setup](#set-up) steps should download `pytest` for you. 

We are using a separate `tests` directory to store all the tests. This directory is intended to mirror the `src` directory to make it easier to find the tests for a specific module.

> [!WARNING]  
> running the `pytest` tests only works when running the service locally (not through the Docker setup)

To run the tests, change to the `/backend` directory and run the following command:

```bash
pytest
```

More documentation on `pytest` can be found [here](https://docs.pytest.org/en/8.0.x/).

## Contributing

### Type errors

The vscode extension [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) can be used to highlight basic type errors in your python code. To set this up do the following:

- Install the extension
- Add the following to your `../.vscode/settings.json` file:

```json
{
    "python.analysis.typeCheckingMode": "basic",
}
```