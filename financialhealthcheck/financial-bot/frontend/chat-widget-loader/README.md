# sBot Chat Widget Loader

Derived from the chatscope example chat widget loader.
See in samples folder and on GitHub at [chatscope/example-chat-widget](https://github.com/chatscope/example-chat-widget) 

## Prerequisites
- NodeJS
- Yarn

## How to run?
### `npm i`

Installs the packages

### `yarn start`

Runs the app in the development mode.  
Open [http://localhost:5000](http://localhost:5000) to view it in the browser.

## Running with only npm

```bash
npm update
npm audit fix --force
npm start
```

You may change default port from ```3000``` to something else

```bash
export PORT=3005 # Unix
$env:PORT=3005 # Windows - Powershell
```

```npm update``` will update dependancies and will change package.json and so on.

Tested on node 19.3.

