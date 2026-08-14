# Connecting to a link

The smallest useful Frost program. Three devices and a `FrostLink` start up,
the devices register with the link, and each reports when it is connected.

Nothing here is application logic — it is the handshake every Frost program
begins with, made visible.

*Adapted from `test/src/TestFrostLink.lf` on Frost's `dev` branch.*

## The program

```lf-python title="src/Main.lf"
target Python {
    fast: true,
    timeout: 1 h
}

import FrostLink from "../frost/src/lib/FrostLink.lf"
import FrostReactor from "../frost/src/lib/FrostReactor.lf"

preamble {=
    from frost import *
=}

reactor Device extends FrostReactor {
    '''A device that registers to the FrostLink and reports when connected.'''

    logical action check_connection

    reaction (startup) -> check_connection {=
        self.logger.info(f"{self._get_reactor_name()} starting up.")
        check_connection.schedule(0)
    =}

    reaction (check_connection) -> check_connection {=
        if self.connected:
            self.logger.info(f"{self._get_reactor_name()} is connected.")
            return 0
        check_connection.schedule(SEC(1))
    =}

    reaction (shutdown) {=
        if not self.connected:
            raise Exception(f"{self._get_reactor_name()} never connected.")
    =}
}

main reactor {
    device_1 = new Device(name="device_1")
    device_2 = new Device(name="device_2")
    device_3 = new Device(name="device_3")
    link = new FrostLink(name="frost_link", width=3)

    device_1.channel_out, device_2.channel_out, device_3.channel_out -> link.channel_in after 0
    link.channel_out -> device_1.channel_in, device_2.channel_in, device_3.channel_in
}
```

## What to notice

**`Device` does not implement registration.** It only polls `self.connected`.
The broadcast, the acknowledgements and the bookkeeping are all inherited from
[`FrostReactor`](../components/frost-reactor.md#registration-and-target-discovery).

**Polling on a logical action, not a timer.** `check_connection.schedule(SEC(1))`
reschedules only while still unconnected, so the poll stops once the handshake
finishes. A timer would keep firing.

**`width=3` on the link matches the three devices.** Each device occupies one
port index, and that index is what the link's routing map stores.

**The `after 0` on one connection.** Both directions need a delay to break the
cycle between the devices and the link; `after 0` introduces a microstep rather
than logical time, which is the cheapest way to do it.

**Failure is loud.** The `shutdown` reaction raises if registration never
completed. `FrostReactor` gives up after 10 attempts and only logs a warning, so
a component that quietly never connects is otherwise easy to miss.

## The data models

Every component needs one, including the link. The link's must have the shape
[`FrostLink`](../components/frost-link.md#the-links-data-model) expects:

```yaml title="resources/data_model/link.yml"
name: "frost_link"
machine_category: "unknown"
machine_type: "unknown"
machine_model: "unknown"
description: ""
root:
  !!FolderNode
  name: "FrostLink"
  description: ""
  children:
    - !!NumericalVariableNode
      name: "#Nodes"
      description: ""
      measure_unit: "NoneMeasureUnits.NONE"
      initial_value: 0
    - !!FolderNode
      name: "NodeInfo"
      description: ""
```

The devices have nothing to expose yet, so their models can be nearly empty —
but they must exist, because `FrostNode` stops the program if the file is
missing:

```yaml title="resources/data_model/device_1.yml"
name: "device_1"
machine_category: "unknown"
machine_type: "unknown"
machine_model: "unknown"
description: ""
root:
  !!FolderNode
  name: "Machine"
  description: ""
  children:
    - !!BooleanVariableNode
      name: "ready"
      initial_value: false
```

Copy it for `device_2` and `device_3`, changing `name:`.

## The configuration

Paths to the data models live here, not in the `.lf` file:

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
    parameters:
      data_model_path: "resources/data_model/device_1.yml"
  device_2:
    parameters:
      data_model_path: "resources/data_model/device_2.yml"
  device_3:
    parameters:
      data_model_path: "resources/data_model/device_3.yml"
```

Paths are resolved relative to the working directory the program runs in.

## Running it

```bash
lfc src/Main.lf
FROST_CONFIG=resources/frost_config.yml bin/Main
```

Each device logs that it is connected once every output port has a registered
peer.

## Next

[Invoking a method](method-invocation.md) — sending an application message once
connected.
