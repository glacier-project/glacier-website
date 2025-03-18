Synchronous method invocation:
``` mermaid
sequenceDiagram
    autonumber
    participant A as Actor 
    participant B as Bus
    participant M as Machine
    A->>B: Invoke(method_name, args, kwargs)
    activate B
    B->>M: Invoke(method_name, args, kwargs)
    activate M
    M->>M: Execute(method_name, args, kwargs)
    M->>B: Return(results)
    deactivate M
    B->>A: Return(results)
    deactivate B
```