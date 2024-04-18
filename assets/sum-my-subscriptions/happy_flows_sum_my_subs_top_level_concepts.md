# "What did I spend more on last month, Amazon or Netflix?"

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
    Director -->> Supervisor: solve all tasks
    Supervisor -->> Router: Find 'get Amazon spending' Agent
    Router -->> DatastoreAgent: solve 'get Amazon spending'
    DatastoreAgent -->> Neo4J: getSubscriptionTotalForLastXDays('Amazon', 31)
    Neo4J -->> DatastoreAgent: £65.15
    DatastoreAgent -->> Supervisor: result: £65.15
    Supervisor -->> Router: Find 'get Netflix spending' Agent
    Router -->> DatastoreAgent: solve 'get Netflix spending'
    DatastoreAgent -->> Neo4J: getSubscriptionTotalForLastXDays('Netflix', 31)
    Neo4J -->> DatastoreAgent: £12.99
    DatastoreAgent -->> Supervisor: result: £12.99
    Supervisor -->> Router: Find 'find greater amount' Agent
    Router -->> ComparerTool: ComparerTool.compare('Amazon: £65.15', 'Netflix: £12.99')
    ComparerTool -->> Supervisor: result: 'Amazon > Netflix'
    Supervisor -->> Router: Find the next best step
    Router -->> Supervisor: All tasks complete
    Supervisor -->> Director: Answer is Amazon
    Director -->> UI: 'Amazon > Netflix'
```
