# Invoking a method

A `Caller` invokes `Square(n=6)` on a `Worker`'s data model, through a
`FrostLink`, and reads `36` out of the response.

This is the request/response pattern — a remote procedure call over Frost
messages.

*Adapted from `test/src/TestMethodInvoke.lf` on Frost's `dev` branch.*

## The worker

The worker's whole job is to bind a Python callable to the `Square` method node,
and to run invocations when Frost hands them over.

```lf-python title="src/Main.lf"
reactor Worker extends FrostReactor {
    reaction (startup) {=
        node = self.data_model.get_node("Machine/Square")
        node.callback = lambda n: n * n
    =}

    # FrostReactor queues plain synchronous MethodNode invocations on
    # new_method_request and leaves the invocation to the concrete reactor.
    reaction (new_method_request) -> channel_out {=
        for bank_index, message in new_method_request.value:
            response = self.protocol_mng.handle_message(message)
            assert response is not None
            self._set_channel_out_port(response, channel_out)
    =}
}
```

The second reaction is the one piece of boilerplate a synchronous method costs
you. `Square` is a plain `!!MethodNode`, and Frost does not run those inline
because a synchronous operation may take several logical time steps — so it
queues them and lets you decide when. Running it immediately, as here, is the
simplest choice; a machine whose operation genuinely takes time would start the
work here and reply when it finished.

An `!!AsyncMethodNode` or `!!CompositeMethodNode` would need no such reaction.

## The caller

```lf-python
reactor Caller extends FrostReactor {
    state target_node = ""       # from parameters.target_node
    state correlation_id
    logical action wait_conn

    reaction (startup) -> wait_conn {=
        wait_conn.schedule(0)
    =}

    reaction (wait_conn) -> wait_conn, channel_out {=
        if not self.connected:
            wait_conn.schedule(MSEC(100))
            return 0

        msg = self.message_builder.build_invoke_method_message(
            target=self.target_node,
            node="Machine/Square",
            args=[],
            kwargs={"n": 6},
        )
        self.correlation_id = msg.correlation_id
        self._set_channel_out_port(msg, channel_out)
    =}

    reaction (response_messages) {=
        for bank_index, message in response_messages.value:
            if message.correlation_id != self.correlation_id:
                continue
            if message.header.msg_name != MethodMsgName.COMPLETED:
                continue
            self.logger.info(f"got COMPLETED: {message.payload.ret}")
            assert message.payload.ret["result"] == 36
            lf.request_stop()
    =}
}
```

Four things carry the weight here.

**Wait for `connected` before sending.** A message sent to a target that has not
registered yet is dropped with an error, not queued.

**`self.target_node` comes from configuration.** The caller does not hard-code
who it is calling; `parameters.target_node` supplies the name. Pointing the same
reactor at a different worker means editing YAML, not Lingua Franca.

**Match on `correlation_id`.** The builder puts one on the request and the
responder copies it onto the reply. With more than one call in flight it is the
only way to tell answers apart.

**Return values are keyed by name.** `message.payload.ret["result"]` uses
`result`, the name declared under `returns:` in the data model — not a position.

## The main reactor

```lf-python
main reactor {
    worker = new Worker(name="worker")
    caller = new Caller(name="caller")
    link = new FrostLink(name="frost_link", width=2)

    worker.channel_out, caller.channel_out -> link.channel_in
    link.channel_out -> worker.channel_in, caller.channel_in after 0
}
```

## The data models

The worker's model is the contract. `Square` takes `n` and returns `result`, and
both are variable nodes so they carry names and types:

```yaml title="resources/data_model/worker.yml"
name: "worker"
machine_category: "unknown"
machine_type: "unknown"
machine_model: "unknown"
description: ""
root:
  !!FolderNode
  name: "Machine"
  description: ""
  children:
    - !!MethodNode
      name: "Square"
      description: ""
      parameters:
        - !!NumericalVariableNode
          name: "n"
          initial_value: 0
      returns:
        - !!NumericalVariableNode
          name: "result"
          initial_value: 0
```

The caller exposes nothing, but still needs a model:

```yaml title="resources/data_model/caller.yml"
name: "caller"
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
      name: "done"
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
  worker:
    parameters:
      data_model_path: "resources/data_model/worker.yml"
  caller:
    parameters:
      data_model_path: "resources/data_model/caller.yml"
      target_node: "worker"
```

`target_node` is not a declared reactor parameter — `FrostBase` sets it as an
attribute anyway and logs a warning. Declaring `state target_node = ""` in the
reactor, as the caller does, both documents it and silences the warning.

## Next

[Subscribing to a variable](variable-subscription.md) — being told about changes
instead of asking for them.
