# Target-Initiator Example

This example provides a request-response interaction. In this scenario, an `Initiator` reactor sends a request to a `Target` reactor by invoking one of its methods. The `Target` then processes the request and sends a response back to the `Initiator`. This pattern is often referred to as a Remote Procedure Call (RPC), and it is essential for building systems where components need to query each other for information or trigger actions.

### The `Target` Data Model

The `Target` reactor's data model serves as its public API, defining the methods that other reactors can invoke. In this case, it exposes a single asynchronous method called `answer`, which accepts a string `message` as an argument and is expected to return a string.

```yaml
name: "target"
description: "Target"
root:
  !!FolderNode
  name: "Methods"
  children:
    - !!AsyncMethodNode
      name: "answer"
      description: "Answer to the message"
      parameters:
        - !!StringVariableNode
          name: "message"
          description: "message to answer"
          default_value: ""
      returns:
        - !!StringVariableNode
          name: "return"
          description: "the answer"
```

### The `Initiator` Reactor

The `Initiator` reactor is the client in this interaction. Its role is to initiate the communication by sending a request to the `Target`. At startup, it builds a message to invoke the `answer` method on the `Target`, passing a question as the argument. After sending the request, it waits for a response. When the response arrives, it logs the answer provided by the `Target`.

```lf-python
reactor Initiator extends FrostBase {
    input channel_in
    output channel_out

    reaction(startup) -> channel_out {=
        // Send a message to invoke the "answer" method on the target
        message = FrostMessage(
            sender=self.name,
            target="target",
            // ... message header for method invocation ...
            payload=MethodPayload(
                node="Methods/answer",
                args=["What is your name?"],
                kwargs={},
            ),
        )
        self._set_channel_out_port(message, channel_out)
    =}

    reaction(channel_in) {=
        // Receive the response from the target
        message = channel_in.value[0]
        if message.header.type == MsgType.RESPONSE and message.header.namespace == MsgNamespace.METHOD:
            self.logger.info(f"{message.sender}: {message.payload.ret['response']}")
    =}
}
```

### The `Target` Reactor

The `Target` reactor is the server in this scenario. It is responsible for implementing the logic of the `answer` method. At startup, it retrieves the `answer` method node from its data model and assigns a callback function to it. When the `Initiator` (or any other reactor) invokes this method, the assigned callback is executed. In this simple example, the callback ignores the input message and returns a fixed string, "Bob".

```lf-python
reactor Target extends FrostMachine {
    state method_node
    state target_name = "Bob"

    reaction(startup) {=
        method_node = self.data_model.get_node("Methods/answer")
        method_node.callback = self.answer
    =}

    method answer(message) {=
        // This method is called when the initiator invokes "Methods/answer"
        return self.target_name
    =}
}
```

### The `main` Reactor

The `main` reactor is responsible for assembling the entire simulation. It instantiates the `Initiator`, `Target`, and a `FrostBus`. The `FrostBus` acts as a message broker, facilitating communication between the other reactors. The `main` reactor connects the `Initiator` and `Target` to the bus, which allows the `Initiator`'s method invocation to be routed to the `Target`, and the `Target`'s response to be sent back.

```lf-python
main reactor {
    frost_bus = new FrostBus(name = "frost_bus", width = 2)
    initiator = new Initiator(name = "initiator")
    target = new Target(name = "target")

    frost_bus.channel_out -> initiator.channel_in, target.channel_in after 10 msec
    initiator.channel_out, target.channel_out -> frost_bus.channel_in after 10 msec
}
```
