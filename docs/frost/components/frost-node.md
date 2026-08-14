# `FrostNode`

`FrostNode` gives a component its data model. It extends
[`FrostBase`](frost-base.md) and is inherited by both
[`FrostReactor`](frost-reactor.md) and [`FrostLink`](frost-link.md).

It is a **mixin**: it has no ports of its own. It owns the data model and the
protocol manager, and leaves all communication to
[`FrostInterface`](frost-interface.md).

```lf-python
reactor FrostNode(_data_model_path = "", update_interval = 1 s) extends FrostBase
```

| Parameter | Default | Meaning |
| --- | --- | --- |
| `_data_model_path` | `""` | Path to the data model YAML file. Normally set through `parameters.data_model_path` in the configuration file rather than here. |
| `update_interval` | `1 s` | How often the `check_update` timer fires, which is how often pending subscription updates are delivered. |

## Loading

At startup `FrostNode` reads the YAML file at `self.data_model_path`, builds the
data model, and creates a `FrostProtocolMng` over it. If the file does not
exist, it logs an error and stops the program.

```lf-python
self.data_model = DataModelBuilder().get_data_model(self.data_model_path)
self.protocol_mng = FrostProtocolMng(self.data_model)
```

Two attributes result, and both are the ones you use in your own reactions:

| Attribute | What it is |
| --- | --- |
| `self.data_model` | The `DataModel` object. Use `get_node(path)` to reach a variable or method. |
| `self.protocol_mng` | Translates `FrostMessage`s into data model operations and back. |

## Reaching nodes

```lf-python
reaction (startup) {=
    # A variable node: read and write it through .value
    self.temperature = self.data_model.get_node("Machine/temperature")

    # A method node: bind a Python callable to its callback
    self.data_model.get_node("Machine/Square").callback = lambda n: n * n
=}
```

Holding onto the node object in a state variable, as above, is the usual
pattern: `get_node` walks the tree by path, so doing it once at startup is
cheaper than doing it in a timer reaction.

Writing to `node.value` is all that is needed to notify subscribers. The change
is recorded by the data model, and the next `check_update` tick turns it into
`UPDATE` messages — see [`FrostReactor`](frost-reactor.md#delivering-updates).

## The component's name

`FrostNode` overrides `_get_reactor_name()` to return the **data model's** name
rather than the reactor's `name` parameter. This is the name other components
must use as a message target.

They are normally the same, because the configuration file keys a component's
section by its reactor name and points it at a data model with a matching
`name:` field. Keeping them in step avoids a class of confusing routing
failures: a component whose data model is named differently from its reactor
will register under the data model name, and messages sent to the reactor name
will not reach it.

Before the data model has loaded, `_get_reactor_name()` falls back to the
reactor's `name`, so startup-time callbacks do not fail.

!!! note "`FrostNode` replaced `FrostDataModel`"

    In Frost v1.0.0 this role was filled by `FrostDataModel`, which extended
    `FrostInterface` and therefore had ports. Splitting the data model out as a
    port-less mixin is what allows `FrostReactor` and `FrostLink` to combine it
    with the interface independently. See
    [Versions](../../reference/versions.md).
