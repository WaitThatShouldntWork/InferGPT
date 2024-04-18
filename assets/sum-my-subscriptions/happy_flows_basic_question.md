## "Hello! What can you do?"

I am a user who is asking about the bots capabilities

### Find tasks from question
```mermaid
sequenceDiagram
    box Purple Frontend
    participant UI
    end
    box DarkBlue Main backend logic
    participant Director
    end
    UI -->> Director: Hello! What can you do?
    Director -->> Director: Return pure-LLM response
    Director -->> UI: I'm InferGPT and can...
```
