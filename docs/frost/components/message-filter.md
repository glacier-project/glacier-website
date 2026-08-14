# `MessageFilter`

`MessageFilter` is the triage stage in front of every Frost component. It
extends [`FrostBase`](frost-base.md) and is instantiated automatically by
[`FrostInterface`](frost-interface.md) — you do not create one yourself.

Its job is to take a stream of incoming messages and answer two questions for
each: *is this for me?* and *what kind of message is it?*

## Ports

| Port | Direction | Purpose |
| --- | --- | --- |
| `message_type` | in | The Python type messages must be an instance of. `FrostInterface` sets it to `FrostMessage`. |
| `filter_callbacks` | in | A list of predicates. A message must satisfy all of them to be accepted. |
| `messages` | in | Incoming `(bank_index, message)` pairs. |
| `requests` | out | Accepted messages whose header type is `REQUEST`. |
| `responses` | out | Accepted messages whose header type is `RESPONSE`. |
| `errors` | out | Accepted messages whose header type is `ERROR`. |
| `discarded_messages` | out | Everything else. |

## What gets discarded

A message goes to `discarded_messages` when it is malformed, when it is not an
instance of `message_type`, or when any filter callback rejects it.

`FrostInterface` installs exactly one callback, which accepts a message only if
its `target` equals this component's name:

```lf-python
message_filter.filter_callbacks.set(
    [lambda msg: is_target_valid(msg, self._get_reactor_name())]
)
```

To narrow further — accepting only certain senders, or only certain
namespaces — a subclass can set a longer list of callbacks. Each is a callable
taking the `(bank_index, message)` pair and returning a boolean.

!!! important "`discarded_messages` is not a dead-letter port"

    Frost uses it for real work. Registration broadcasts are addressed to the
    marker `"__target__"` rather than to a component's own name, so the target
    filter rejects them and they surface here. Both
    [`FrostReactor`](frost-reactor.md) and [`FrostLink`](frost-link.md) react to
    `discarded_messages` to implement registration — and `FrostLink` additionally
    forwards anything else it finds there towards that message's target, which
    is how routing works at all.

    If you react to `discarded_messages` in your own component, ignore anything
    that is not yours and leave the rest alone.

## Nested payloads

If a message's payload is itself a list, the filter expands it in place and
processes each element separately. This lets a component send a batch on one
port and have it arrive as individual messages.
