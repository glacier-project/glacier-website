# `FrostBus` Reactor

The `FrostBus` is a central component in the Frost architecture that acts as a message router. It is responsible for managing the registration of different Frost components and ensuring that messages are delivered to their intended targets. It extends `FrostDataModel`, allowing it to have its own data model for tracking registered machines.

### Core Functionalities

- **Component Registration**: The `FrostBus` listens for registration requests from other Frost components. When a component sends a `REGISTER` message, the bus adds it to a `routing_map`, which maps the component's name to its bus index.
- **Message Routing**: It overrides the `_set_channel_out_port` method to implement its routing logic. When it receives a message to send, it looks up the target in its `routing_map` and forwards the message to the correct output port connected to that target.
- **Data Model Management**: The bus maintains a data model that keeps track of the number of registered machines and information about each one, such as its index on the bus.

### Code Snippets

**Handling Registration Requests**

This reaction processes registration requests from new components, adding them to the routing map and updating the data model.

```lf-python
reaction(message_filter.requests) -> channel_out {=
    for bank_index, message in message_filter.requests.value:
        if message.header.namespace != MsgNamespace.PROTOCOL or message.header.msg_name != ProtocolMsgName.REGISTER:
            continue
        
        if message.sender in self.routing_map:
            continue

        self.routing_map[message.sender] = bank_index
        
        # ... update data model with new machine info ...

        self.number_of_machines.value += 1

        # Send a response to acknowledge the registration
        response = FrostMessage(
            # ... create response message ...
        )
        self._set_channel_out_port([response], channel_out)
=}
```

**Message Routing**

This method contains the core routing logic. It looks up the message's target in the `routing_map` and sends the message to the corresponding output port.

```lf-python
method _set_channel_out_port(value, channel_out) {=
    for message in value:
        if message.target not in self.routing_map:
            self.logger.warning(f"Cannot route message {message} to unknown target {message.target}.")
            continue

        index = self.routing_map[message.target]
        self._set_output_port(message, channel_out[index])
=}
```
