# `MessageFilter` Reactor

The `MessageFilter` is a specialized reactor designed to process and route incoming Frost messages. It acts as a gatekeeper, examining each message and directing it to the appropriate output port based on its type and content. This allows for a clean separation of concerns, as reactors can subscribe to specific types of messages (requests, responses, or errors) without needing to parse every incoming message themselves.

### Core Functionalities

- **Message-Type Filtering**: It categorizes messages based on their header type (`REQUEST`, `RESPONSE`, `ERROR`) and forwards them to corresponding output ports (`requests`, `responses`, `errors`).
- **Custom Filtering Logic**: Supports custom filter callbacks that allow for more advanced filtering based on message content, sender, or other criteria. Messages that do not meet the filter criteria are sent to a `discarded_messages` port.
- **Decoupling**: By handling the initial message triage, it decouples the message-receiving logic from the message-processing logic within other reactors.

### Code Snippets

**Handling Messages**

This reaction is the core of the `MessageFilter`. It iterates through incoming messages, applies the filter callbacks, and routes each message to the appropriate output port.

```lf-Python
reaction (messages) -> requests, responses, errors, discarded_messages {=
    for message in messages.value:
        if not isinstance(message[1], self._message_type):
            self.logger.warning(f"Invalid message type: {type(message[1])}")
            continue

        if self._should_process_message(message):
            self._handle_message(message, requests, responses, errors)
        else:
            self._set_output_port(message, discarded_messages)
=}
```

**Custom Filter Application**

This method checks if a message should be processed by applying a series of user-defined filter callbacks.

```lf-Python
method _should_process_message(message) {=
    for callback in self._filter_callbacks:
        if not callback(message):
            return False
    return True
=}
```
