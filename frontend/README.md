# Frontend

UI service for interfacing with InferGPT.

## Set up

1. Create the `.env` files. There are template files (.env.example) for you to copy with comments for guidance. If you are running the service in Docker you can skip the rest of the setup.

2. Change directory to the `/backend` space, then run the following to install the dependencies

```bash
npm install
```

3. Run the app using

```bash
npm start
```

Check the frontend app is running at [http://localhost:8650](http://localhost:8650)

### Frontend Linting

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
