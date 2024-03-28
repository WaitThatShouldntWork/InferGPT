# Frontend
UI service for a chat bot.

# Run Locally

Checkout the code and run the following commands from the root of the frontend directory:

```bash
npm install
npm start
```

The app should now be running on [localhost:8650](http://localhost:8650/).

# Connect to Backend

To connect to the backend you will need to have the correct `.env` file locally. To do this:

- Make a copy of the `.env.example` file in the root of the frontend directory and name it `.env`
- Update the values in your `.env` file

# Code linting

We have set up ESLint. To run the linter, run the following command:

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
