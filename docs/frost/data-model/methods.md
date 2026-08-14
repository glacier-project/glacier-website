# Methods

A method node is an operation a machine exposes. Declaring one in the data model
publishes it; binding a Python callable to its `callback` gives it behaviour.

Three kinds exist, and they differ in **when the caller gets an answer**.

| Tag | Returns | Use for |
| --- | --- | --- |
| `!!MethodNode` | When the operation has finished | Operations that produce a result |
| `!!AsyncMethodNode` | Immediately; completion is observed elsewhere | Commands that start something |
| `!!CompositeMethodNode` | When its control-flow graph finishes | Sequences built from other nodes |

## Declaring a method

Parameters and return values are themselves variable nodes, which is how they
carry names, types, descriptions and units.

```yaml
- !!MethodNode
  name: "Square"
  description: "Return the square of n"
  parameters:
    - !!NumericalVariableNode
      name: "n"
      initial_value: 0
  returns:
    - !!NumericalVariableNode
      name: "result"
      initial_value: 0
```

## Binding behaviour

```python
node = data_model.get_node("Machine/Square")
node.callback = lambda n: n * n
print(node(3))
```

Inside a Frost component, bind it at startup:

```lf-python
reaction (startup) {=
    self.data_model.get_node("Machine/Square").callback = lambda n: n * n
=}
```

The callback's parameters must match the names declared under `parameters`, so
that a caller can pass arguments by keyword.

Method nodes also support pre- and post-call callbacks, in the same way
[variables](nodes.md#read-and-write-callbacks) support pre- and post-access
callbacks.

## Invoking over Frost

```lf-python
msg = self.message_builder.build_invoke_method_message(
    target="worker",
    node="Machine/Square",
    args=[],
    kwargs={"n": 6},
)
self._set_channel_out_port(msg, channel_out)
```

The result comes back as a `METHOD`/`COMPLETED` response, and the return values
are in `message.payload.ret`, keyed by the names declared under `returns`:

```lf-python
reaction (response_messages) {=
    for bank_index, message in response_messages.value:
        if message.correlation_id != self.correlation_id:
            continue
        if message.header.msg_name == MethodMsgName.COMPLETED:
            self.logger.info("result = %s", message.payload.ret["result"])
=}
```

`correlation_id` is set on the message the builder returns, and copied onto the
response. Keep it if you have more than one call in flight.

See the [method invocation example](../examples/method-invocation.md).

!!! note "Synchronous methods need a reaction in your component"

    A plain `!!MethodNode` invocation is queued on `FrostReactor`'s
    `new_method_request` logical action instead of being run inline, because a
    synchronous operation may span several time steps. Your component decides
    when to run it. `!!AsyncMethodNode` and `!!CompositeMethodNode` need no such
    reaction. See
    [`FrostReactor`](../components/frost-reactor.md#handling-requests).

## Asynchronous methods

```yaml
- !!AsyncMethodNode
  name: "start_cycle"
  description: "Begin a production cycle"
  parameters:
    - !!StringVariableNode
      name: "recipe"
      default_value: ""
  returns:
    - !!BooleanVariableNode
      name: "accepted"
```

An asynchronous method returns as soon as it is invoked. Whatever it set in
motion completes later, and the caller observes that completion some other way —
usually by [subscribing](nodes.md#subscriptions) to a variable the operation
updates.

This models a real machine command well: `start_cycle` is acknowledged in
milliseconds, and the cycle it starts takes a minute.

## Composite methods

A composite method is defined as a **control-flow graph** over other nodes,
rather than as a Python callback. It runs the graph and returns when the graph
finishes — so it gives a synchronous interface to a sequence built from
asynchronous parts.

```yaml
- !!CompositeMethodNode
  name: "stamp_workpiece"
  description: "Load, stamp and release a workpiece"
  parameters:
    - !!StringVariableNode
      name: "material"
      default_value: "aluminium"
  cfg:
    - !!WriteVariableNode
      variable: "Machine/press/command"
      value: 1
    - !!WaitConditionNode
      variable: "Machine/press/position"
      operator: "=="
      rhs: 100
    - !!ReadVariableNode
      variable: "Machine/press/force"
      store_as: "force"
  returns:
    - !!NumericalVariableNode
      name: "force"
```

### Control-flow node types

| Tag | Keys | Effect |
| --- | --- | --- |
| `!!ReadVariableNode` | `variable`, `store_as` | Read a variable into a named slot in the execution scope |
| `!!WriteVariableNode` | `variable`, `value` | Write a variable |
| `!!WaitConditionNode` | `variable`, `operator`, `rhs` | Block until the comparison holds |
| `!!CallMethodNode` | `method`, `args`, `kwargs` | Invoke another method on this data model |

There are remote counterparts — `!!CallRemoteMethodNode`,
`!!ReadRemoteVariableNode`, `!!WriteRemoteVariableNode` and
`!!WaitRemoteEventNode` — which perform the same operations against **another
component's** data model over Frost messages. A composite method can therefore
orchestrate several machines.

### Suspension and resumption

If the graph reaches a `!!WaitConditionNode` whose condition is not yet
satisfied, execution suspends. In that case the call returns the **id of the
execution instance** rather than the declared return values. When the condition
later becomes true the execution resumes, and the results are delivered then.

A caller must therefore be prepared for both shapes of answer. This is the
mechanism by which one call can span the minutes a physical operation takes,
while the data model keeps track of where the sequence got to.
