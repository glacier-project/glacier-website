# `FrostBase`

`FrostBase` is the root of the Frost component hierarchy. It provides the
utilities every other reactor relies on: a logger, configuration handling, port
helpers and logical-time helpers. It has no ports of its own.

```lf-python
reactor FrostBase(name = "unnamed_reactor")
```

| Parameter | Default | Meaning |
| --- | --- | --- |
| `name` | `"unnamed_reactor"` | The component's identifier. Used as the logger name, as the key into the configuration file, and — for components that communicate — as the address other components send messages to. |

## Logging

At startup `FrostBase` creates `self.logger`, a standard Python
`logging.Logger` named after the reactor, and sets its level from the
configuration file. Use it rather than `print`, so that output is timestamped
with logical time and can be silenced per component.

```lf-python
self.logger.info("Received %s", value)
```

## Configuration

`FrostBase` also reads the reactor's own section of the configuration file at
startup and applies it. Two things are applied: the `logging_level`, and any
entries under `parameters`, which are set as attributes on the reactor.

The lookup walks the reactor's name as a dotted path, so nested reactors get
nested configuration:

```yaml title="frost_config.yml"
logging_level: INFO
reactors:
  device_1:
    logging_level: INFO
    parameters:
      data_model_path: "resources/data_model/device_1.yml"
      peer: "device_2"
    reactors:
      message_filter:
        logging_level: WARNING
```

With that file, a reactor named `device_1` gets `self.data_model_path` and
`self.peer` set before its own startup reactions run, and its message filter is
quieter than it is.

If a `parameters` key does not correspond to an existing attribute, it is still
set, and a warning is logged. This is how a state variable declared with a
placeholder gets its real value:

```lf-python
reactor Device extends FrostReactor {
    # Supplied through parameters.peer in the configuration file.
    state peer = ""
}
```

See [Configuration](../configuration.md) for the full file format.

## Sending on ports

Reactions rarely assign to output ports directly. `FrostBase` provides helpers
that accumulate values instead of overwriting them, which matters because
several reactions in the inheritance chain may write to the same port at the
same logical tag.

| Method | Purpose |
| --- | --- |
| `_set_output_port(value, port)` | Append `value` (or extend, if it is a list) to `port`. Fans out to every port if `port` is a multiport. |
| `_set_output_multiport(value, port, exclude)` | Append to every port of a multiport, skipping the indices in `exclude`. |
| `_set_channel_out_port(value, channel_out)` | Send on the component's outgoing channel. `FrostReactor` and `FrostLink` override this to route by target — always use it rather than writing to `channel_out` directly. |
| `_get_input_values(port)` | Read a port as a list of `(bank_index, value)` pairs, skipping absent ports. |

## Logical time

Frost components run on Lingua Franca's logical clock. `FrostBase` exposes it in
a few units:

```lf-python
self._get_current_logical_time_ns()
self._get_current_logical_time_us()
self._get_current_logical_time_ms()
self._get_current_logical_time_sec()
self._get_current_logical_time_min()
self._get_current_logical_time_hour()
self._get_current_logical_time(unit)   # unit: a TimePrecision value
```

These report elapsed logical time, not wall-clock time. Under `fast: true` a
simulated hour passes in a fraction of a second of real time, and these helpers
report the simulated hour.

## When to extend it directly

Extend `FrostBase` for a component that needs logging and configuration but not
Frost messaging — typically a model driven by plain Lingua Franca ports from a
parent reactor. For anything that participates in the Frost network, extend
[`FrostReactor`](frost-reactor.md) instead.
