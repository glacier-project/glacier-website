# Data model

The machine data model is the interface between a machine and everything that
talks to it. It is a tree of nodes — folders, variables and methods — declared
in a YAML file, inspired by the OPC UA information model.

Every Frost component owns one. Reading a machine's state means reading a
variable in its data model; commanding it means invoking a method.

[:octicons-mark-github-16: glacier-project/machine-data-model](https://github.com/glacier-project/machine-data-model)

!!! info "A standalone library"

    `machine-data-model` is a Python library in its own right, with no
    dependency on Frost or on Lingua Franca. It can be used on its own to
    describe and drive a machine — including a real one, through a
    [connector](connectors.md). Frost is one consumer of it.

    Latest release: **v1.0.0**. These pages document the `dev` branch, which is
    the repository's default branch.

## A model in full

```yaml title="machine.yml"
name: "worker"
machine_category: "unknown"
machine_type: "unknown"
machine_model: "unknown"
description: "A machine that squares numbers"
root:
  !!FolderNode
  name: "Machine"
  description: ""
  children:
    - !!NumericalVariableNode
      name: "temperature"
      description: "Current temperature"
      measure_unit: "TemperatureUnits.DegreeCelsius"
      initial_value: 20.0

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

The top-level keys describe the machine; `root` holds the tree. Nodes are tagged
with the YAML tag of the class to build — `!!FolderNode`,
`!!NumericalVariableNode`, `!!MethodNode` and so on.

Nodes are addressed by path from the root node, using `/` as the separator:
`Machine/temperature`, `Machine/Square`. Note that the path starts with the
**root node's `name`** (`Machine` here), not with the machine's `name`
(`worker`).

## Using it

Outside Frost, load a model with the builder:

```python
from machine_data_model.builder.data_model_builder import DataModelBuilder

data_model = DataModelBuilder().get_data_model("machine.yml")

node = data_model.get_node("Machine/temperature")
node.value = 21.5

data_model.write_variable("Machine/temperature", 22.0)
print(data_model.read_variable("Machine/temperature"))
```

Inside Frost, [`FrostNode`](../components/frost-node.md) does the loading, and
the model is available as `self.data_model`.

## The node types

| Tag | Holds |
| --- | --- |
| `!!FolderNode` | Other nodes. The root is always a folder. |
| `!!NumericalVariableNode` | A number, optionally with a measurement unit and a valid range. |
| `!!StringVariableNode` | A string. |
| `!!BooleanVariableNode` | A boolean. |
| `!!ObjectVariableNode` | Named properties, each itself a variable node. |
| `!!MethodNode` | A synchronous operation. |
| `!!AsyncMethodNode` | An operation that returns immediately and completes later. |
| `!!CompositeMethodNode` | An operation defined as a control-flow graph over other nodes. |

!!! warning "There is no `!!VariableNode` or `!!ObjectNode` tag"

    `VariableNode` is the abstract base class of the four variable types; it is
    not something you can write in YAML. An object is
    `!!ObjectVariableNode`.

## Read on

<div class="grid cards" markdown>

-   __Variables and folders__

    ---

    Declaring state, measurement units, subscriptions and read/write callbacks.

    [:octicons-arrow-right-24: Variables and folders](nodes.md)

-   __Methods__

    ---

    Synchronous, asynchronous and composite methods, and how to bind behaviour
    to them.

    [:octicons-arrow-right-24: Methods](methods.md)

-   __Connectors__

    ---

    Backing a node with a real OPC UA server or MQTT broker.

    [:octicons-arrow-right-24: Connectors](connectors.md)

</div>
