# Example chat widget

A repository dedicated to the series of articles about web widgets.  

The series is available here:  
[Web widgets (Part 1): What is it?](https://chatscope.io/blog/web-widgets-part-1-what-is-it/)  
[Web widgets (Part 2): Widget him!](https://chatscope.io/blog/web-widgets-part-2-widget-him/)  
[Web widgets (Part 3): API Cookbook](https://chatscope.io/blog/web-widgets-part-3-api-cookbook/)  

You will also need second repository containing widget loader, which is available here:  
[https://github.com/chatscope/example-widget-loader](https://github.com/chatscope/example-widget-loader)  

## How to run?
### `yarn start`

Runs the app in the development mode.  
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.  

The page will reload if you make edits.  
You will also see any lint errors in the console.

Note: This requires Node.js v16 installed. As well as yarn.

### Running with only npm

```bash
npm update
npm audix fix --force
npm start
```

```npm update``` will update dependancies and will change package.json and so on. 

Tested on node 19.3.

# sBOT Updates
Have tweaked the Widget Container to allow for connection to OpenAI API. We will remove this for the true front end once the back end is in place.
