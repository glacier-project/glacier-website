# Configuration

Every Frost program reads one YAML configuration file at startup. It supplies
the things that would otherwise be hard-coded in `.lf` files: where each
component's data model lives, how loudly each one logs, and any per-component
parameters.

Keeping them here means the same Lingua Franca sources can be run against
different plants, different models or different logging levels without editing
code.

## Where the file is found

Frost reads the path from the `FROST_CONFIG` environment variable, defaulting to
`resources/frost_config.yml`:

```bash
FROST_CONFIG=resources/frost_config.yml bin/Main
```

If the file does not exist, Frost falls back to built-in defaults
(`time_precision: NSECS`, `logging_level: WARNING`) and every component uses an
empty data model path — which then fails when `FrostNode` tries to load it. A
missing configuration file is therefore worth ruling out first when a program
stops immediately at startup.

Paths inside the file are resolved relative to the process's working directory,
not to the file's own location.

## The file

```yaml title="resources/frost_config.yml"
time_precision: NSECS
logging_level: INFO

reactors:
  frost_link:
    logging_level: WARNING
    parameters:
      data_model_path: "resources/data_model/link.yml"
    reactors:
      message_filter:
        logging_level: WARNING

  device_1:
    logging_level: INFO
    parameters:
      data_model_path: "resources/data_model/device_1.yml"
      peer: "device_2"
    reactors:
      message_filter:
        logging_level: WARNING
```

### Top level

| Key | Meaning |
| --- | --- |
| `time_precision` | The unit logical timestamps are formatted in. One of `NSECS`, `USECS`, `MSECS`, `SECS`, `MINUTES`, `HOURS`. |
| `logging_level` | The default level for every component. Standard Python names: `DEBUG`, `INFO`, `WARNING`, `ERROR`. |
| `reactors` | Per-component sections, keyed by component name. |

### Per component

| Key | Meaning |
| --- | --- |
| `logging_level` | Overrides the global level for this component. |
| `parameters` | Entries set as attributes on the reactor before its own startup reactions run. |
| `reactors` | Sections for reactors *contained* in this one. |

Lookup follows the component's name as a dotted path, which is why a contained
reactor nests. Every Frost component contains a `MessageFilter` named
`<component>.message_filter`, and it is the usual thing to quieten — it logs
every message it sees at `DEBUG`.

## `parameters`

Entries under `parameters` are applied with `setattr`, so they can set any
attribute the reactor has — and any it does not.

**`data_model_path` is the one every component needs.** It is how
[`FrostNode`](components/frost-node.md) finds its YAML model.

**Anything else is yours.** Declare a state variable with a placeholder, supply
the real value here:

```lf-python
reactor Device extends FrostReactor {
    state peer = ""          # from parameters.peer
}
```

Setting a key the reactor does not have still works, and logs a warning:

```text
Parameter peer not found in reactor device_1. Creating dynamic parameter peer = device_2.
```

Declaring the state variable is worth it: it documents what the component
expects, and keeps the log clean.

!!! warning "Timers and widths cannot be set here"

    `parameters` are applied in a startup reaction, which runs after the reactor
    has been built. Anything used to construct the reactor — a timer period such
    as `update_interval`, or a multiport `width` — must be passed at
    instantiation instead:

    ```lf-python
    link = new FrostLink(name="frost_link", width=3)
    ```

## Names must agree

Three names have to line up for a component to be reachable:

1. the `name` passed at instantiation — `new Device(name="device_1")`;
2. the key under `reactors:` in this file — `device_1:`;
3. the `name:` field of the data model that component loads.

The first two must match or the component gets no configuration, and will fail
to load a data model. The first and third must match or the component registers
under one name while everyone addresses it by another — because
[`FrostNode`](components/frost-node.md#the-components-name) reports the data
model's name as the component's identity.

## Logging

`self.logger` is a standard Python logger, and Frost installs a formatter that
prefixes each line with the current logical time in `time_precision` units. That
is what makes a Frost log readable: entries are ordered by simulated time, not
by when they happened to be flushed.

Turn a single component up without drowning in the rest:

```yaml
logging_level: WARNING
reactors:
  device_1:
    logging_level: DEBUG
```
