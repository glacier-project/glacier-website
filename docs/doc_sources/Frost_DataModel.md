# `FrostDataModel` Reactor

The `FrostDataModel` reactor is a key component in the Frost framework that integrates a data model into a reactor. It extends `FrostInterface`, inheriting its communication capabilities, and adds functionality for managing and interacting with a data model defined in an external file. This allows reactors to maintain state, expose methods, and react to changes in a structured and organized way.

### Core Functionalities

- **Data Model Loading**: At startup, it loads a data model from a specified YAML file. This data model defines the reactor's state variables, methods, and their initial values.
- **Request Handling**: It processes incoming request messages, such as method invocations or variable read/write requests, and uses a `FrostProtocolMng` to handle the logic.
- **Response Handling**: It processes response messages, which are typically the result of a previous request it sent.
- **Data Model Updates**: It includes a timer to periodically check for updates in the data model and send notifications to any subscribers.

### Code Snippets

**Initializing the Data Model**

This reaction loads the data model from the specified path and initializes the protocol manager.

```lf-python
reaction (startup) {=
    if not os.path.exists(self.data_model_path) and not os.path.isfile(self.data_model_path):
        self.logger.error(f"Data model file not found: {self.data_model_path}")
        lf.request_stop()

    self.data_model = DataModelBuilder().get_data_model(self.data_model_path)
    self.protocol_mng = FrostProtocolMng(self.data_model)
=}
```

**Processing Requests**

This reaction handles incoming request messages from the `MessageFilter`. It distinguishes between different types of requests (e.g., method invocations) and uses the protocol manager to generate a response.

```lf-python
reaction (message_filter.requests) -> channel_out {=
    for bank_index, message in message_filter.requests.value:
        if message.header.namespace == MsgNamespace.PROTOCOL or message.target != self.name:
            continue

        // ... logic to handle different request types ...

        response = self.protocol_mng.handle_request(message)
        self._set_channel_out_port(response, channel_out)
=}
```

**Handling Data Model Updates**

To ensure that subscribers are notified of any changes, the `FrostDataModel` reactor includes a timer, `check_update`, that periodically triggers a reaction to send out update messages. This reaction checks if the protocol manager has any pending update messages, and if so, sends them to the appropriate subscribers via the `channel_out` port.

```lf-python
reaction (check_update) -> channel_out{=
    '''Check if there are any updates in the data model and send them to the subscribers.'''
    
    update_messages = list(self.protocol_mng.get_update_messages())
    if not update_messages:
        return

    self._set_channel_out_port(update_messages, channel_out)
    self.protocol_mng.clear_update_messages()
=}
```
