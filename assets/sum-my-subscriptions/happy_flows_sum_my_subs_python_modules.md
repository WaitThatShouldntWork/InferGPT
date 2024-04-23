# "What did I spend more on last month, Amazon or Netflix?"

I am a user who wants to know if last month I spent more on my Netflix subscription than my Amazon one

### Find tasks from question
```mermaid
sequenceDiagram
```

### Find tasks from question
```mermaid
sequenceDiagram
    box Frontend
    participant server.ts
    end
    box Backend
    participant llm.py
    participant director.py
    participant supervisor.py
    end
    box Backend: Agents and Tools
    participant tasks.py
    end
    server.ts -->> director.py: pass utterance
    director.py -->> llm.py: Is this a processable question?
    llm.py -->> director.py: Yes
    director.py -->> tasks.py: Request list of tasks
    tasks.py -->> llm.py: Split 'What did I spend more on last month, Amazon or Netflix?' into up to 5 goals
    llm.py -->> tasks.py: 1. get Amazon spending, 2. get Netflix spending, 3. find greater amount
    tasks.py -->> director.py: tasks as array
    director.py -->> supervisor.py: solve these tasks
```
    
### Solve step 1. get Amazon spending
```mermaid
sequenceDiagram
    box Backend
    participant supervisor.py
    participant router.py
    participant llm.py
    end
    box Backend: Agents and Tools
    participant datastore_agent.py
    participant graph_db_utils.py
    end
    supervisor.py -->> router.py: Find the Agent I should assign 'get Amazon spending' task to
    router.py -->> llm.py: Determine which agent is best for this task
    llm.py -->> router.py: Use DatastoreAgent
    router.py -->> supervisor.py: Call datastore_agent.py with prompt 'get Amazon spending'
    supervisor.py -->> datastore_agent.py: Find the answer to the following: 'get Amazon spending'
    datastore_agent.py -->> llm.py: Function call: identify methods
    llm.py -->> datastore_agent.py: Use getSubscriptionTotalForLastXDays('Amazon', 31)
    datastore_agent.py -->> graph_db_utils.py: Use getSubscriptionTotalForLastXDays('Amazon', 31)
    graph_db_utils.py -->> datastore_agent.py: £65.15
    datastore_agent.py -->> supervisor.py: method: getSubscriptionTotalForLastXDays('Amazon', 31), result: £65.15
```

### Solve step 2. get Netflix spending
```mermaid
sequenceDiagram
    box Backend
    participant supervisor.py
    participant router.py
    participant llm.py
    end
    box Backend: Agents and Tools
    participant datastore_agent.py
    participant graph_db_utils.py
    end
    supervisor.py -->> router.py: Find the Agent I should assign 'get Netflix spending' task to
    router.py -->> llm.py: Determine which agent is best for this task
    llm.py -->> router.py: Use DatastoreAgent
    router.py -->> supervisor.py: Call datastore_agent.py with prompt 'get Netflix spending'
    supervisor.py -->> datastore_agent.py: Find the answer to the following: 'get Netflix spending'
    datastore_agent.py -->> llm.py: Function call: identify methods
    llm.py -->> datastore_agent.py: Use getSubscriptionTotalForLastXDays('Netflix', 31)
    datastore_agent.py -->> graph_db_utils.py: Use getSubscriptionTotalForLastXDays('Netflix', 31).  Cypher query for Netflix spending in 31 days
    graph_db_utils.py -->> datastore_agent.py: £12.99
    datastore_agent.py -->> supervisor.py: method: getSubscriptionTotalForLastXDays('Netflix' 31), result: £12.99
```

### Solve step 3. find greater amount
```mermaid
sequenceDiagram
    box Frontend
    participant server.ts
    end
    box Backend
    participant director.py
    participant supervisor.py
    participant router.py
    participant llm.py
    end
    box Backend: Agents and Tools
    participant comparer.py
    end
    supervisor.py -->> router.py: Find the Agent I should assign 'find greater amount' task to
    router.py -->> llm.py: Next best step prompt
    llm.py -->> router.py: ComparerTool
    router.py -->> supervisor.py: Use comparer.py with args 'Amazon: £65.15', 'Netflix: £12.99'
    supervisor.py -->> comparer.py: comparer.py.compare('Amazon: £65.15', 'Netflix: £12.99')
    comparer.py -->> supervisor.py: 'Amazon £65.15 is greater than Netflix £12.99 by £52.16'
    supervisor.py -->> router.py: Find the next best step
    router.py -->> llm.py: Next best step prompt
    llm.py -->> router.py: chooses tasks_complete
    router.py -->> supervisor.py: All tasks complete
    supervisor.py -->> director.py: Answer is 'Amazon £65.15 is greater than Netflix £12.99 by £52.16'
    director.py -->> server.ts: return answer
```
