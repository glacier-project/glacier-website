# `FrostBase` Reactor

The `FrostBase` reactor serves as the foundational component for all other reactors in the Frost framework. It provides a set of common utility methods and basic functionalities that are inherited by other, more specialized reactors. Its primary purpose is to offer a standard toolkit for logging, parameter handling, and message passing, ensuring consistency across the entire system.

### Core Functionalities

- **Logging**: Initializes a logger for each reactor instance, allowing for standardized and configurable logging.
- **Parameter Overriding**: Includes a method to override a reactor's default parameters with values from a configuration file. This allows for flexible and centralized configuration management.
- **Message-Passing Utilities**: Provides helper methods like `_set_output_port` and `_get_input_values` to simplify the process of sending and receiving messages through ports, including handling multiport outputs.

### Configuration and Parameter Overriding

One of the key features provided by `FrostBase` is the ability to override a reactor's parameters from an external configuration file. This allows for highly flexible and centralized management of reactor settings without modifying the source code.

#### Configuration File Example

The configuration is typically provided in a YAML file. This file can define settings for multiple reactors, including their logging levels and any custom parameters.

Here is an example of a `config.yml` file:

```yaml
reactors:
  my_reactor_instance:
    logging_level: "DEBUG"
    parameters:
      update_interval: 500  # msec
      threshold: 42.5
```

In this example, we are defining settings for a reactor instance named `my_reactor_instance`. We are setting its logging level to `DEBUG` and overriding two of its parameters: `update_interval` and `threshold`.

#### How It Works

1.  **Loading the Configuration**: At the start of the simulation, this YAML file is loaded into a Python dictionary.
2.  **Passing to the Reactor**: This dictionary is then passed to the reactor, typically during its initialization.
3.  **Overriding Parameters**: The `__override_initial_parameters` method is called within the reactor's startup sequence. This method explores the configuration dictionary to find the section corresponding to the reactor's name. It then dynamically updates the reactor's attributes (`self.update_interval = 500`, `self.threshold = 42.5`) using the values from the file.

This mechanism allows you to easily change reactor behavior for different simulation runs just by modifying the configuration file.

### Code Snippets

**Parameter Overriding Method**

This is the method within `FrostBase` that performs the dynamic parameter update.

```lf-python
method __override_initial_parameters(configuration, reactor_name) {=
    // ... search for the reactor's configuration in the dictionary ...

    if "parameters" not in configuration or not isinstance(configuration["parameters"], dict):
        return

    for key, value in configuration["parameters"].items():
        if not hasattr(self, key):
            self.logger.warning(f"Parameter {key} not found in reactor {reactor_name}. Creating dynamic parameter {key} = {value}.")

        setattr(self, key, value)
=}
```

**Setting Output Port Value**

This utility method simplifies the process of setting or appending values to an output port, which is fundamental for message passing.

```lf-python
method _set_output_port(value, output_port) {=
    '''Set the output value for the specified output port. If a value is already set, it will append the new value to the existing one.'''

    if output_port.width > 0:
        self._set_output_multiport(value, output_port, None)
        return

    if not output_port.is_present:
        output_port.set([])

    if isinstance(value, list):
        output_port.value.extend(value)
    else:
        output_port.value.append(value)
=}
```
