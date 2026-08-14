# Subscribing to a variable

A `Publisher` raises its own `temperature` on a timer. A `Subscriber` asks to be
told when that variable changes, and receives `UPDATE` messages.

This is the publish/subscribe pattern, and it is how monitoring components,
dashboards and alarms observe a plant without polling it.

*Adapted from `test/src/TestSubscription.lf` on Frost's `dev` branch.*

## The publisher

```lf-python title="src/Main.lf"
reactor Publisher extends FrostReactor {
    timer bump(2 sec, 1 sec)
    state temperature

    reaction (startup) {=
        self.temperature = self.data_model.get_node("Machine/temperature")
    =}

    reaction (bump) {=
        if self.connected:
            self.temperature.value += 1
            self.logger.info(f"temperature -> {self.temperature.value}")
    =}
}
```

That is the entire publisher. **There is no publishing code.**

Writing `self.temperature.value` is enough: the data model records the change,
and `FrostReactor`'s `check_update` timer turns it into `UPDATE` messages for
whoever has subscribed. A machine written this way does not know or care whether
anyone is listening.

## The subscriber

```lf-python
reactor Subscriber extends FrostReactor {
    state target_node = ""       # from parameters.target_node
    logical action wait_conn

    reaction (startup) -> wait_conn {=
        wait_conn.schedule(0)
    =}

    reaction (wait_conn) -> wait_conn, channel_out {=
        if not self.connected:
            wait_conn.schedule(MSEC(100))
            return 0

        msg = self.message_builder.build_subscribe_variable_message(
            target=self.target_node,
            node="Machine/temperature",
        )
        self._set_channel_out_port(msg, channel_out)
    =}

    reaction (response_messages) {=
        for bank_index, message in response_messages.value:
            if message.header.namespace == MsgNamespace.VARIABLE \
                    and message.header.msg_name == VariableMsgName.UPDATE:
                self.logger.info(f"received UPDATE: {message.payload}")
    =}
}
```

**The node path is the publisher's, not the subscriber's.**
`"Machine/temperature"` is a path inside the *target's* data model; `target`
says whose. The two components happen to both use `Machine` as their root folder
name, which is convention, not a requirement.

**Updates keep arriving on `response_messages`.** An `UPDATE` is not a reply to
anything the subscriber just sent — it is unsolicited. Frost still classifies it
as a response, so one reaction handles both the subscription acknowledgement and
the stream that follows. Filter on `msg_name` to tell them apart.

## The main reactor

```lf-python
main reactor {
    publisher = new Publisher(name="publisher")
    subscriber = new Subscriber(name="subscriber")
    link = new FrostLink(name="frost_link", width=2)

    publisher.channel_out, subscriber.channel_out -> link.channel_in
    link.channel_out -> publisher.channel_in, subscriber.channel_in after 0
}
```

## The data models

```yaml title="resources/data_model/publisher.yml"
name: "publisher"
machine_category: "unknown"
machine_type: "unknown"
machine_model: "unknown"
description: ""
root:
  !!FolderNode
  name: "Machine"
  description: ""
  children:
    - !!NumericalVariableNode
      name: "temperature"
      description: ""
      initial_value: 20
```

```yaml title="resources/data_model/subscriber.yml"
name: "subscriber"
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

The link uses the model shown in
[Connecting to a link](link-registration.md#the-data-models).

## The configuration

```yaml title="resources/frost_config.yml"
time_precision: NSECS
logging_level: INFO
reactors:
  frost_link:
    logging_level: WARNING
    parameters:
      data_model_path: "resources/data_model/link.yml"
  publisher:
    parameters:
      data_model_path: "resources/data_model/publisher.yml"
  subscriber:
    parameters:
      data_model_path: "resources/data_model/subscriber.yml"
      target_node: "publisher"
```

## Timing

The publisher bumps `temperature` every second, but updates leave on the
`check_update` timer, which fires every `update_interval` — one second by
default, from [`FrostNode`](../components/frost-node.md).

Those two rates are independent. If the variable changed ten times within one
interval, the subscriber would see the value at the end of it, not ten updates.
This is a design decision, not a limitation: it bounds message volume when a
simulated machine updates state on a fast timer.

To notify more finely, lower `update_interval` on the publishing component. This
one is a Lingua Franca parameter rather than a configuration entry, because it
sets a timer period, which is fixed when the reactor is instantiated:

```lf-python
publisher = new Publisher(name="publisher", update_interval = 100 msec)
```

!!! note "Not everything can move to the configuration file"

    Values that a reactor uses to build its own structure — timer periods,
    multiport widths — are needed before the configuration file is read, so they
    must be passed at instantiation. `parameters:` entries are applied in a
    startup reaction, which is early enough for data model paths and plain state
    variables, but too late for a timer.

## Beyond plain change notification

The data model also supports notifying only when a value enters or leaves a
range, which suits alarms better than a notification per change. See
[Kinds of subscription](../data-model/nodes.md#kinds-of-subscription).
