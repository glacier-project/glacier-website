# `FrostReactor` Reactor

The `FrostReactor` is a base component for Frost actors that need to communicate over the `FrostBus`. It extends the `FrostInterface` and provides the essential logic for a reactor to initialize itself and establish a connection with the bus at startup.

### Core Functionalities

- **Automatic Bus Connection**: The primary feature of `FrostReactor` is its automatic connection to the `FrostBus`. At startup, it triggers a logical action `connect_to_bus`, which is handled by the parent `FrostInterface` to begin the registration process.
- **Initialization Logging**: It logs an informational message upon initialization, which is helpful for debugging and tracking the lifecycle of reactors.

### Code Snippet

This reaction is triggered at startup and is responsible for initiating the connection to the `FrostBus`.

```lf-python
reaction (startup) -> connect_to_bus {=
    '''Initialize the reactor and trigger connection to the FrostBus.'''
    self.logger.info(f"Initializing FrostReactor: {self._get_reactor_name()}")

    # Trigger the connection to the bus.
    connect_to_bus.schedule(0)
=}
```
