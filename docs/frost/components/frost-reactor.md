# `FrostReactor`

`FrostReactor` is the component you extend. It combines
[`FrostInterface`](frost-interface.md), which gives it channels and message
dispatch, with [`FrostNode`](frost-node.md), which gives it a data model. On top
of those it adds registration, routing, data-model request handling and
subscription updates.

A simulated machine, a scheduler, a monitoring application and a test harness
are all `FrostReactor`s. They differ in the data model they load and the
reactions you write.

```lf-python
reactor FrostReactor(_update_step = 1000 msec) extends FrostInterface, FrostNode
```

| Parameter | Default | Meaning |
| --- | --- | --- |
| `_update_step` | `1000 msec` | The retry interval for registration. Available afterwards as `self.update_step`. |

## State you can read

| Attribute | Meaning |
| --- | --- |
| `self.connected` | `True` once every output port has a registered peer. Wait for this before sending application messages. |
| `self.targets` | `{peer name: port index}` for every peer discovered so far. |
| `self.data_model` | This component's data model. |
| `self.message_builder` | Builds `FrostMessage`s addressed from this component. |
| `self.protocol_mng` | Applies messages to the data model. |

## Writing a component

```lf-python title="Machine.lf"
reactor Machine extends FrostReactor {
    state temperature

    reaction (startup) {=
        self.temperature = self.data_model.get_node("Machine/temperature")
        self.data_model.get_node("Machine/Square").callback = lambda n: n * n
    =}

    timer tick(2 sec, 1 sec)

    reaction (tick) {=
        if self.connected:
            self.temperature.value += 1
    =}
}
```

That is the whole pattern: bind data model nodes at startup, then change them
from timers and reactions. Frost turns the changes into messages.

## Registration and target discovery

A `FrostReactor` learns its neighbours before it can address them by name.

At startup it broadcasts a `PROTOCOL`/`REGISTER` request on **every** output
port, addressed not to a component but to the marker `"__target__"`. Because
that is not any component's name, each recipient's
[`MessageFilter`](message-filter.md) discards it — and both `FrostReactor` and
`FrostLink` react to `discarded_messages` to pick it up, record the sender
against the port it arrived on, and acknowledge it.

Discovery is therefore bidirectional and symmetric: a component learns its peers
both from the answers to its own broadcast and from the broadcasts it receives.

Every `update_step` the component checks whether all its output ports have been
accounted for. When they have, it sets `self.connected`. If they have not after
**10 attempts**, it logs a warning and stops retrying — `self.connected` stays
`False` and messages to unknown targets are dropped with an error.

So application logic waits:

```lf-python
logical action wait_conn

reaction (startup) -> wait_conn {=
    wait_conn.schedule(0)
=}

reaction (wait_conn) -> wait_conn, channel_out {=
    if not self.connected:
        wait_conn.schedule(MSEC(100))
        return 0
    msg = self.message_builder.build_invoke_method_message(
        target="worker", node="Machine/Square", args=[], kwargs={"n": 6},
    )
    self._set_channel_out_port(msg, channel_out)
=}
```

## Routing

`FrostReactor` overrides `_set_output_multiport`, so `_set_channel_out_port`
picks a port per message:

1. if the message's target is in `self.targets`, send on that port — **direct
   delivery, bypassing the link**;
2. otherwise, if a peer named `frost_link` is known, send there and let the
   [link](frost-link.md) route it;
3. otherwise log an error and drop the message.

This is why a link is optional: components wired directly to each other find
each other during discovery and never involve a router.

!!! warning "The fallback peer is matched by name"

    Step 2 looks for a peer literally named `frost_link`. A `FrostLink`
    instantiated under a different name will still be discovered as a target and
    will still route messages sent explicitly to it, but it will not act as the
    default route for unknown targets.

## Handling requests

Incoming `VARIABLE` and `METHOD` requests arrive on the `request_messages`
logical action, and `FrostReactor` handles almost all of them for you: it passes
each to `self.protocol_mng.handle_message(message)` and sends the response back.
Reads, writes, subscriptions, asynchronous methods and composite methods all
work with no code on your part beyond declaring them in the data model.

There is one exception. A **plain synchronous `MethodNode`** may take several
logical time steps to complete, so Frost does not run it inline. Those
invocations are queued on the `new_method_request` logical action and left to
you:

```lf-python
reaction (new_method_request) -> channel_out {=
    for bank_index, message in new_method_request.value:
        response = self.protocol_mng.handle_message(message)
        self._set_channel_out_port(response, channel_out)
=}
```

Running the method immediately, as above, is the simplest implementation. A
long-running method would instead start the work here and reply once it
finishes.

!!! note

    `AsyncMethodNode` and `CompositeMethodNode` invocations do **not** arrive on
    `new_method_request`; they are handled by the protocol manager directly.

## Delivering updates

`FrostNode`'s `check_update` timer fires every `update_interval`. On each tick
`FrostReactor` asks the protocol manager for pending update messages, sends
them, and clears the queue.

A subscriber therefore sees a variable's changes at the granularity of
`update_interval`, not instantaneously. If several writes happen within one
interval, the subscriber sees the state at the end of it. Lower
`update_interval` for finer-grained notification, at the cost of more messages.

!!! note "`FrostReactor` absorbed `FrostMachine`"

    Frost v1.0.0 distinguished `FrostReactor` (communication only) from
    `FrostMachine` (communication plus a data model). The current `FrostReactor`
    is the merger of the two. See [Versions](../../reference/versions.md).
