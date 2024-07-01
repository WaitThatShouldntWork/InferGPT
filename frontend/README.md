# Frontend

UI service for interfacing with InferGPT.

## Set up

1. Ensure the `.env` file has been configured as described in the main [README](../README.md).

This README covers instructions on how to run the application:
- Locally
- In a Docker Container

For ease of use, we would recommended that you run the entire application using **Docker Compose** instead. See main [README](../README.md).

If you would prefer not to use **Docker Compose**, read on...

## Running Locally

1. Change directory to the `/frontend` space, then run the following to install the dependencies

```bash
npm install
```

2. Run the app using

```bash
npm start
```

Check the frontend app is running at [http://localhost:8650](http://localhost:8650)

## Running in a Docker Container

1. Build the Docker image

```bash
docker build -t {my-frontend-image-name} .
```

2. Run the app within a Docker container

```bash
docker run --env-file ../.env -p 8650:8650 {my-frontend-image-name}
```

> Note that we pass in the entire environment file that contains all our application's configuration. This means some unneccessary configuration is also being passed in. This is fine when testing locally. In production, we must limit this to only the essential frontend configuration (see environment configuration within [Docker Compose](../compose.yml)).

Check the frontend app is running at [http://localhost:8650](http://localhost:8650)

## Frontend Linting

We have set up ESLint for the frontend ccode. To run the linter, use the following command:

```bash
npm run lint
```

This will attempt to fix any errors you have and will also show you any errors that it can't fix. To automatically fix errors on save (for vscode) do the following:

- create a `.vscode` folder in the root of the project
- create a `settings.json` file in the `.vscode` folder
- add the following to the `settings.json` file:

```json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```
