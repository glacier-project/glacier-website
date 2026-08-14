# Connectors

A connector backs data model nodes with a real system. The node API does not
change: a variable is still read with `read()`, written with `write()` and
subscribed to in the same way, whether it holds a simulated value or maps onto
an OPC UA node or an MQTT topic.

This is what lets control software developed against a simulated plant be
pointed at real equipment without being rewritten.

Two connectors are implemented: **OPC UA** and **MQTT**.

## How a model uses one

A model declares its connectors at the top level, then attaches nodes to them.
A node inherits `connector_name` from its ancestors, so tagging the root folder
is usually enough. `remote_resource_spec` says where on the remote system that
particular node lives.

```yaml
connectors:
  - !!OpcUaConnector
    name: "opc_ua_server"
    ip: "127.0.0.1"
    port: 4840

root:
  !!FolderNode
  name: "Objects"
  connector_name: "opc_ua_server"
  children:
    - !!NumericalVariableNode
      name: "Temperature"
      default_value: 20.0
    - !!BooleanVariableNode
      name: "StartCommand"
      default_value: false
      remote_resource_spec:
        !!OpcUaRemoteResourceSpec
        node_id: "ns=2;s=StartCommand"
```

## OPC UA

Variables map to OPC UA nodes; reads and writes are performed against them, and
method calls are performed against OPC UA method nodes.

The connector is built on [`asyncua`](https://github.com/FreeOpcUa/opcua-asyncio),
pinned at 1.1.6.

Runnable examples, including an OPC UA server to test against, are in
[`examples/opcua/`](https://github.com/glacier-project/machine-data-model/tree/dev/examples/opcua)
and [`examples/ice/`](https://github.com/glacier-project/machine-data-model/tree/dev/examples/ice).

## MQTT

Variables map to MQTT topics. A read returns the last payload received on the
subscribe topic; a write publishes to the publish topic.

```yaml
connectors:
  - !!MqttConnector
    name: "mqtt_broker"
    ip: "127.0.0.1"
    port: 1883
    topic_prefix: "machines/boiler-1"
    payload_codec: "string"

root:
  !!FolderNode
  name: "Objects"
  connector_name: "mqtt_broker"
  children:
    - !!BooleanVariableNode
      name: "StartCommand"
      default_value: false
      remote_resource_spec:
        !!MqttRemoteResourceSpec
        subscribe_topic: "plant/line-1/start/state"
        publish_topic: "plant/line-1/start/set"
```

Payloads are encoded with one of three codecs, selected by `payload_codec`:

| Codec | Behaviour |
| --- | --- |
| `string` (default) | Strings, integers, floats and booleans as UTF-8 scalars. Values received on a subscription are parsed according to the data model node's type. |
| `json` | JSON. |
| `msgpack` | MessagePack. |

For anything else, `MqttConnector` accepts `payload_serializer` and
`payload_deserializer` callables from Python.

Beyond `ip`, `port` and `topic_prefix`, the connector accepts `username`,
`password`, `client_id`, `keepalive`, `qos` and `retain`, and each of the
connection settings has an `_env_var` variant (`ip_env_var`, `port_env_var`,
`username_env_var`, `password_env_var`) that reads the value from an environment
variable instead — so credentials need not be committed alongside the model.

### Two current limitations

!!! warning

    **Method calls are not supported by the MQTT connector.** A model reached
    over MQTT can expose variables, not operations.

    **Topic wildcards are not supported** in remote resource specs. Each node
    names its own topics.

## Choosing between them

OPC UA is the richer fit: it has a node model close to the data model's own, and
it carries methods as well as variables. MQTT suits equipment and gateways that
already publish to a broker, where only telemetry and simple commands are needed.

Both connectors are asynchronous underneath, and both present the same
synchronous node API.
