# Variables and folders

## Folders

A folder holds other nodes and gives the model its shape. The root of every data
model is a folder.

```yaml
root:
  !!FolderNode
  name: "Machine"
  description: "The machine's interface"
  children:
    - !!FolderNode
      name: "statistics"
      children:
        - !!NumericalVariableNode
          name: "checks"
          initial_value: 0
```

Folders nest freely. The path to a node is its ancestors' names joined with `/`,
starting at the root node: `Machine/statistics/checks`.

## Variables

Four concrete variable types exist. Each stores a value and can be read,
written and subscribed to.

=== "Numerical"

    ```yaml
    - !!NumericalVariableNode
      name: "temperature"
      description: "Current temperature"
      measure_unit: "TemperatureUnits.DegreeCelsius"
      initial_value: 20.0
    ```

=== "String"

    ```yaml
    - !!StringVariableNode
      name: "batch_id"
      description: "Identifier of the batch being processed"
      initial_value: ""
    ```

=== "Boolean"

    ```yaml
    - !!BooleanVariableNode
      name: "running"
      description: "Whether the machine is running"
      initial_value: false
    ```

=== "Object"

    ```yaml
    - !!ObjectVariableNode
      name: "workpiece"
      description: "The workpiece currently held"
      properties:
        - !!StringVariableNode
          name: "material"
          initial_value: "aluminium"
        - !!BooleanVariableNode
          name: "stamped"
          initial_value: false
    ```

### Keys

| Key | Applies to | Meaning |
| --- | --- | --- |
| `name` | all | The node's name, and the segment used in its path. |
| `description` | all | Free text. |
| `id` | all | An explicit identifier. Generated if omitted. |
| `initial_value` | all variables | The starting value. |
| `default_value` | all variables | Used as the starting value if `initial_value` is absent. |
| `measure_unit` | numerical | A unit, written as `"<UnitsEnum>.<Member>"`, e.g. `"LengthUnits.Meter"`. Defaults to `NoneMeasureUnits.NONE`. |
| `properties` | object | The object's child variables. |
| `connector_name` | all | Binds the node to a [connector](connectors.md). |
| `remote_resource_spec` | all | Where the node lives on the remote system. See [connectors](connectors.md). |

!!! tip "Unknown keys are an error, not a typo you get to keep"

    The builder raises `ValueError: Unexpected keys: …` if a node carries a key
    that type does not accept, and lists the allowed ones. A misspelled
    `inital_value` fails loudly at load time rather than silently leaving the
    variable at its default.

## Reading and writing

In Python, a variable node behaves like a value holder:

```python
node = data_model.get_node("Machine/temperature")
node.value = 21.5
print(node.value)
```

or through the model:

```python
data_model.write_variable("Machine/temperature", 22.0)
print(data_model.read_variable("Machine/temperature"))
```

`read()` and `write()` are also available, and are what the connector layer
uses; for a node backed by a remote system they perform the remote operation.

Object properties are reached with bracket notation:

```python
workpiece = data_model.get_node("Machine/workpiece")
print(workpiece["material"].value)
```

## Subscriptions

A subscriber asks to be told when a variable changes, instead of polling it.

Over Frost, that is a `VARIABLE`/`SUBSCRIBE` request, and the notifications come
back as `VARIABLE`/`UPDATE` messages:

```lf-python
msg = self.message_builder.build_subscribe_variable_message(
    target="publisher",
    node="Machine/temperature",
)
self._set_channel_out_port(msg, channel_out)
```

```lf-python
reaction (response_messages) {=
    for bank_index, message in response_messages.value:
        if message.header.namespace == MsgNamespace.VARIABLE \
                and message.header.msg_name == VariableMsgName.UPDATE:
            self.logger.info("temperature is now %s", message.payload.value)
=}
```

See the [subscription example](../examples/variable-subscription.md) for a
complete program.

Updates are not instantaneous. The publishing component accumulates them and
flushes them on its `check_update` timer, which fires every `update_interval` —
see [`FrostReactor`](../components/frost-reactor.md#delivering-updates).

### Kinds of subscription

The library distinguishes several event types (`DATA_CHANGE`, `IN_RANGE`,
`OUT_OF_RANGE`, `ANY`) and provides `DataChangeSubscription` and
`RangeSubscription` alongside the base `VariableSubscription`. A range
subscription notifies when a value crosses into or out of a band, rather than on
every change — useful for alarms.

The `examples/subscription/` directory of the
[machine-data-model repository](https://github.com/glacier-project/machine-data-model/tree/dev/examples/subscription)
has runnable programs for data-change notifications, range notifications,
hierarchical notifications, scoped subscriptions and unsubscription.

## Read and write callbacks

A variable can run your code around each access. This is how a simulated
machine makes a variable *mean* something.

```python
node.set_pre_read_value_callback(lambda: print("about to be read"))
node.set_post_read_value_callback(lambda value: print("was read:", value))
node.set_pre_update_value_callback(lambda new_value: print("about to write", new_value))
node.set_post_update_value_callback(lambda prev, new: prev != new)
```

The post-update callback returns a boolean, and returning `False` **cancels the
write**: the node reverts to its previous value. That makes it the natural place
for validation — rejecting a setpoint outside the machine's operating envelope,
for instance.
