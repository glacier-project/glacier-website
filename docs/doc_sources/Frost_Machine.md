# `FrostMachine` Reactor

The `FrostMachine` reactor is a composite component that combines the functionalities of `FrostDataModel` and `FrostReactor`. It is designed to serve as a base for creating "machine" actors in the Frost ecosystem—components that have both a data model and the ability to communicate over the `FrostBus`.

### Core Functionalities

- **Inheritance**: It inherits from both `FrostDataModel` and `FrostReactor`, giving it the combined capabilities of both. This means it can manage a data model, connect to the `FrostBus`, and handle messages according to the Frost protocol.
- **Update Step**: It introduces an `update_step` parameter, which can be used to define a time step for periodic updates within the machine. This is useful for simulations or for components that need to perform actions at regular intervals.

### Code Snippet

The definition of the `FrostMachine` reactor is straightforward, as it primarily relies on inheritance to acquire its functionality.

```lf-python
reactor FrostMachine(_update_step = 1000 msec) extends FrostDataModel, FrostReactor {
    '''Reactor implementing the common logic for Frost machines.
    
    Args:
        _update_step (int): The time step for periodic updates in the machine.
    '''

    state update_step = _update_step
}
```
