# `FrostLink`

`FrostLink` is the message router of a Frost network. Components register with
it, and it forwards each message to whichever port its target sits behind.

Like [`FrostReactor`](frost-reactor.md), it combines
[`FrostInterface`](frost-interface.md) with [`FrostNode`](frost-node.md) — it has
channels *and* a data model, which it uses to publish what has registered.

You instantiate it rather than extending it.

```lf-python
link = new FrostLink(name="frost_link", width=3)

device_1.channel_out, device_2.channel_out, device_3.channel_out -> link.channel_in after 0
link.channel_out -> device_1.channel_in, device_2.channel_in, device_3.channel_in
```

`width` must equal the number of components wired to the link.

!!! tip "Name it `frost_link`"

    A `FrostReactor` sends messages for unknown targets to a peer named
    literally `frost_link`. Using that name is what makes the link the default
    route.

## Registration

Registration reaches the link the same way it reaches any component: a
`PROTOCOL`/`REGISTER` request addressed to the marker `"__target__"`, which the
[`MessageFilter`](message-filter.md) discards and the link picks up from
`discarded_messages`.

For each new sender the link records `routing_map[sender] = port index`, adds an
entry to its data model, increments the node count, and acknowledges on the port
the request arrived on.

## Routing

`FrostLink` overrides `_set_channel_out_port`. For each outgoing message it
looks up `message.target` in `routing_map` and sends on the corresponding port.
A message for an unregistered target is dropped with a warning:

```text
Cannot route message ... to unknown target ...
```

Messages to route are the ones that arrive in `discarded_messages` and are not
registrations — that is, messages addressed to *some other* component, which
the link's own target filter therefore rejected. Rejection and forwarding are
the same event seen from two sides.

## The link's data model

`FrostLink` requires a data model with a specific shape, because it writes into
it at startup:

```yaml title="link.yml"
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

Three paths must exist — `FrostLink`, `FrostLink/#Nodes` and
`FrostLink/NodeInfo` — and the link looks them up by exactly those names. As
components register, it adds a folder under `NodeInfo` named after each one,
containing a numeric `Index` node, and keeps `#Nodes` current.

This means the routing table is itself readable over Frost: a monitoring
component can subscribe to `FrostLink/#Nodes` to watch the network form.

Point the link at this file through `parameters.data_model_path` in the
[configuration file](../configuration.md), like any other component.

!!! note "`FrostLink` replaced `FrostBus`"

    Frost v1.0.0 called this component `FrostBus`, and its data model used
    `#Machines` / `MachineInfo` rather than `#Nodes` / `NodeInfo`. See
    [Versions](../../reference/versions.md).
