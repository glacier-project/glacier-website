# `FrostInterface` Reactor

The `FrostInterface` reactor establishes the fundamental communication protocol for all Frost components. It extends `FrostBase` and introduces a standardized way for reactors to connect to the `FrostBus` and handle incoming and outgoing messages. This reactor is crucial for ensuring that all components in the system can communicate reliably and consistently.

### Core Functionalities

- **Bus Connection Management**: Implements the logic for a reactor to register itself with the `FrostBus`. It includes a handshake mechanism that repeatedly attempts to connect until it succeeds or times out.
- **Message Filtering**: Incorporates a `MessageFilter` reactor to process incoming messages. This allows for routing messages based on their type (e.g., requests, responses, errors) and other custom criteria.
- **Standardized Communication Ports**: Defines `channel_in` and `channel_out` ports for receiving and sending messages, providing a consistent interface for all reactors.

### Code Snippets

**Connecting to the Bus**

This reaction handles the process of registering the reactor with the `FrostBus`. It sends a registration request and schedules a retry if the connection is not immediately established.

```lf-python
reaction(connect_to_bus) -> channel_out, connect_to_bus {=
    if self.connected:
        return

    if lf.time.logical_elapsed() > SEC(9):
        raise Exception(f"Handshake failed: {self.name} unable to connect to the bus")
    
    self._set_channel_out_port(self._create_registration_message(), channel_out)
    connect_to_bus.schedule(SEC(3))
=}
```

**Processing Incoming Messages**

This reaction forwards all incoming messages from the `channel_in` port to the `MessageFilter` for further processing.

```lf-python
reaction (channel_in) -> message_filter.messages {=
    values = self._get_input_values(channel_in)
    messages = [(bank_index, m) for bank_index, bank_msgs in values for m in bank_msgs]
    self._set_output_port(messages, message_filter.messages)
=}
```
