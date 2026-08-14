# Examples

Three complete programs, each showing one thing.

<div class="grid cards" markdown>

-   __Connecting to a link__

    ---

    The smallest useful Frost program: three components register with a
    `FrostLink` and report when they are connected.

    [:octicons-arrow-right-24: Connecting to a link](link-registration.md)

-   __Invoking a method__

    ---

    A caller invokes a method on another component's data model and checks the
    result that comes back.

    [:octicons-arrow-right-24: Invoking a method](method-invocation.md)

-   __Subscribing to a variable__

    ---

    A subscriber asks to be told when another component's variable changes,
    and receives updates.

    [:octicons-arrow-right-24: Subscribing to a variable](variable-subscription.md)

</div>

## Where these come from

These examples are adapted from Frost's own test suite, on the `dev` branch —
`test/src/TestFrostLink.lf`, `test/src/TestMethodInvoke.lf` and
`test/src/TestSubscription.lf`. Frost's CI builds and runs them on every push,
so they are known to work against the code they document.

Adaptations are limited to trimming the assertions that make them tests, and
naming files as you would in a project of your own.

## Running them

Each example needs three files:

```text
your-project/
├── src/
│   └── Main.lf                       the program
└── resources/
    ├── frost_config.yml              logging, data model paths, parameters
    └── data_model/
        ├── link.yml                  the FrostLink's data model
        └── ...                       one per component
```

Build and run with the Lingua Franca compiler:

```bash
lfc src/Main.lf
FROST_CONFIG=resources/frost_config.yml bin/Main
```

`FROST_CONFIG` defaults to `resources/frost_config.yml`, so if you keep that
path you can leave the variable out. See [Configuration](../configuration.md).

!!! tip "Start from the template"

    [frost-template](https://github.com/glacier-project/frost-template) is a
    GitHub template with this layout, Frost as a submodule, and a main reactor
    already in place.

## Other examples

[frost-playground](https://github.com/glacier-project/frost-playground) collects
larger examples — publisher/subscriber, sensor/alarm, a stock-market toy and a
production scheduler.

!!! warning "The playground targets Frost v1.0.0"

    Its Frost submodule is pinned to the `main` branch, so its examples use the
    v1.0.0 component names (`FrostMachine`, `FrostBus`, `FrostDataModel`) rather
    than the ones documented here. They do not compile against `dev` unchanged.
    See [Versions](../../reference/versions.md).
