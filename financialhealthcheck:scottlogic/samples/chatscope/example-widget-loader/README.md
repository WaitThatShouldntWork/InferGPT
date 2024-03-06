# Example widget loader

A repository dedicated to the series of articles about web widgets.  

The series is available here:  
[Web widgets (Part 1): What is it?](https://chatscope.io/blog/web-widgets-part-1-what-is-it/)  
[Web widgets (Part 2): Widget him!](https://chatscope.io/blog/web-widgets-part-2-widget-him/)  
[Web widgets (Part 3): API Cookbook](https://chatscope.io/blog/web-widgets-part-3-api-cookbook/)  

You will also need second repository containing widget, which is available here:  
[https://github.com/chatscope/example-chat-widget](https://github.com/chatscope/example-chat-widget)  

## How to run?
### `yarn start`

Runs the app in the development mode.  
Open [http://localhost:5000](http://localhost:5000) to view it in the browser.

## Running with only npm

```bash
npm update
npm audix fix --force
npm start
```

You may change default port from ```3000``` to something else

```bash
export PORT=3005 # Unix
$env:PORT=3005 # Windows - Powershell
```

```npm update``` will update dependancies and will change package.json and so on.

Tested on node 19.3.
