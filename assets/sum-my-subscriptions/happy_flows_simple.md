# Sequence diagrams of the happy flow

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

## "What did I spend more on last month, Amazon or Netflix?"

I am a user who wants to know if last month I spent more on my Netflix subscription than my Amazon one

### Find tasks from question
```mermaid
sequenceDiagram
```

```mermaid
sequenceDiagram
    box Purple Frontend
    participant UI
    end
    box DarkBlue Main backend logic
    participant Director
    participant Supervisor
    participant Router
    end
    box DarkBlue Agents and Tools
    participant TaskAgent
    participant DatastoreAgent
    participant ComparerTool
    end
    box Brown Databases
    participant Neo4J
    end
    UI -->> Director: pass utterance
    Director -->> TaskAgent: Request list of tasks
    TaskAgent -->> Director: tasks as array
    Director -->> Supervisor: tasks
    Supervisor -->> Router: Find the Agent I should assign 'get Amazon spending' task to
    Router -->> Router: Determine which agent is best for this task
    Router -->> Supervisor: Call DatastoreAgent with prompt 'get Amazon spending'
    Supervisor -->> DatastoreAgent: Find the answer to the following: 'get Amazon spending'
    DatastoreAgent -->> DatastoreAgent: Function call: identify methods
    DatastoreAgent -->> Neo4J: Use getSubscriptionTotalForLastXDays('Amazon', 31). Cypher query for Amazon spending in 31 days
    Neo4J -->> DatastoreAgent: £65.15
    DatastoreAgent -->> Supervisor: method: getSubscriptionTotalForLastXDays('Amazon', 31), result: £65.15
    Supervisor -->> Router: Find the Agent I should assign 'get Netflix spending' task to
    Router -->> Router: Determine which agent is best for this task
    Router -->> Supervisor: Call DatastoreAgent with prompt 'get Netflix spending'
    Supervisor -->> DatastoreAgent: Find the answer to the following: 'get Netflix spending'
    DatastoreAgent -->> DatastoreAgent: Function call: identify methods
    DatastoreAgent -->> Neo4J: Use getSubscriptionTotalForLastXDays('Netflix', 31). Neo4J: Cypher query for Netflix spending in 31 days
    Neo4J -->> DatastoreAgent: £12.99
    DatastoreAgent -->> Supervisor: method: getSubscriptionTotalForLastXDays('Netflix' 31), result: £12.99
    Supervisor -->> Router: Find the Agent I should assign 'find greater amount' task to
    Router -->> Router: Next best step prompt
    Router -->> Supervisor: Use ComparerTool with args 'Amazon: £65.15', 'Netflix: £12.99'
    Supervisor -->> ComparerTool: ComparerTool.compare('Amazon: £65.15', 'Netflix: £12.99')
    ComparerTool -->> Supervisor: 'Amazon £65.15 is greater than Netflix £12.99 by £52.16'
    Supervisor -->> Router: Find the next best step
    Router -->> Router: Next best step prompt
    Router -->> Supervisor: All tasks complete
    Supervisor -->> Director: Answer is 'Amazon £65.15 is greater than Netflix £12.99 by £52.16'
    Director -->> UI: return answer
```
