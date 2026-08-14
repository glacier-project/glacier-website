# `FrostInterface`

`FrostInterface` gives a component its communication channels and sorts what
arrives on them. It extends [`FrostBase`](frost-base.md) and is inherited by
both [`FrostReactor`](frost-reactor.md) and [`FrostLink`](frost-link.md).

```lf-python
reactor FrostInterface(width = 1) extends FrostBase
```

| Parameter | Default | Meaning |
| --- | --- | --- |
| `width` | `1` | The number of ports in each channel. A component wired to one peer needs width 1; a `FrostLink` serving three components needs width 3. |

## Channels

```lf-python
input[width]  channel_in
output[width] channel_out
```

Both channels are multiports. Each index is one link to one peer, and Frost uses
the index a message arrived on to learn where that peer is — see
[registration](frost-reactor.md#registration-and-target-discovery).

Messages are sent with `_set_channel_out_port`, never by assigning to
`channel_out` directly, because subclasses override that method to route by
target.

## Dispatch

Everything that arrives on `channel_in` is flattened into `(bank_index, message)`
pairs and handed to a private [`MessageFilter`](message-filter.md). The filter
drops anything that is not a `FrostMessage` addressed to this component, and
splits the rest into requests, responses and errors.

`FrostInterface` then splits those again by namespace, and schedules four
logical actions:

| Logical action | Carries |
| --- | --- |
| `request_messages` | Requests in the `VARIABLE` and `METHOD` namespaces — the ones that act on the data model |
| `response_messages` | Responses in those namespaces |
| `request_protocol_messages` | Requests in the `PROTOCOL` namespace — registration and similar |
| `response_protocol_messages` | Responses in the `PROTOCOL` namespace |

Writing a component means reacting to these actions rather than to `channel_in`:

```lf-python
reaction (response_messages) {=
    for bank_index, message in response_messages.value:
        if message.header.namespace == MsgNamespace.VARIABLE \
                and message.header.msg_name == VariableMsgName.UPDATE:
            self.logger.info("update: %s", message.payload)
=}
```

Splitting on a logical action rather than dispatching inline keeps each concern
in its own reaction, and lets Lingua Franca schedule them explicitly.

!!! note "Subscription confirmations"

    A `VARIABLE`/`SUBSCRIBE` response is logged and then passed on to
    `response_messages` like any other response. `_validate_subscription` is a
    hook a subclass can override to reject one; the base implementation accepts
    everything.

## Target registration

`FrostInterface` maintains `self.targets`, a dictionary mapping a peer's name to
the port index it was seen on. Every message that arrives adds its sender to
that map if it is not already there. `FrostReactor` uses the map to deliver
messages directly to a known peer.

## The message builder

`self.message_builder` is a `FrostMessageBuilder` bound to this component's
name, so messages it produces are already addressed from the right sender:

```lf-python
msg = self.message_builder.build_invoke_method_message(
    target="worker",
    node="Machine/Square",
    args=[],
    kwargs={"n": 6},
)
self._set_channel_out_port(msg, channel_out)
```

The builder comes from
[machine-data-model](https://github.com/glacier-project/machine-data-model);
`FrostNode` replaces it with the protocol manager's own builder once the data
model has loaded.
