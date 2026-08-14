# Frost

Frost is an open-source framework for developing, testing and deploying the
software that controls and supervises industrial machines. It lets you build
that software against a virtual plant — a digital twin — and validate it before
running it on real equipment.

Frost is a library of [Lingua Franca](https://www.lf-lang.org/) reactors. Lingua
Franca is a coordination language whose programs execute deterministically over
a logical clock, which is what makes a Frost scenario reproducible.

[:octicons-mark-github-16: glacier-project/frost](https://github.com/glacier-project/frost)

!!! info "This documentation follows the `dev` branch"

    `dev` is Frost's default branch and its current line of development. The
    released version, v1.0.0, has different component names. See
    [Versions](../reference/versions.md) before copying code into a project that
    pins a release.

## The shape of a Frost program

A Frost program is a Lingua Franca main reactor that instantiates components and
wires their channels together. Everything you write extends `FrostReactor`.

```lf-python title="Main.lf"
target Python {
    fast: true,
    timeout: 1 h
}

import FrostLink from "../../src/lib/FrostLink.lf"
import FrostReactor from "../../src/lib/FrostReactor.lf"

preamble {=
    from frost import *
=}

reactor Machine extends FrostReactor {
    reaction (startup) {=
        # Bind a Python function to a method declared in the data model.
        self.data_model.get_node("Machine/Square").callback = lambda n: n * n
    =}
}

main reactor {
    machine = new Machine(name="machine")
    link = new FrostLink(name="frost_link", width=1)

    machine.channel_out -> link.channel_in
    link.channel_out -> machine.channel_in after 0
}
```

Three things are worth noticing.

**A component's name is its address.** `name="machine"` is both the reactor's
identifier and the target other components put in the messages they send it.

**The data model is not passed here.** Each component's data model file is named
in the [configuration file](configuration.md), keyed by the component's name.
This keeps a `.lf` file free of paths.

**`FrostLink` has a `width`.** It is a multiport router: `width` must match the
number of components wired to it.

## Where to go

<div class="grid cards" markdown>

-   :material-cube-outline: __Components__

    ---

    The six reactors Frost provides, what each one contributes, and how they
    inherit from each other.

    [:octicons-arrow-right-24: Components](components/index.md)

-   :material-file-tree: __Data model__

    ---

    Declaring a machine's variables and methods in YAML, and connecting them to
    OPC UA or MQTT.

    [:octicons-arrow-right-24: Data model](data-model/index.md)

-   :material-code-braces: __Examples__

    ---

    Worked programs: registering with a link, invoking a method, subscribing to
    a variable.

    [:octicons-arrow-right-24: Examples](examples/index.md)

-   :material-cog-outline: __Configuration__

    ---

    The YAML file that supplies data model paths, logging levels and per-component
    parameters.

    [:octicons-arrow-right-24: Configuration](configuration.md)

</div>

## Requirements

Frost needs the Lingua Franca compiler, a JDK for it to run on, and Python.

| Requirement | Version |
| --- | --- |
| Lingua Franca (`lfc`) | installed via `curl -Ls https://install.lf-lang.org \| bash -s cli` |
| Java | 17 (the version Frost's CI uses) |
| Python | 3.12 or later (Frost's CI tests 3.12 and 3.13) |
| `make` | for the test targets |

Python dependencies are installed with `pip install -r requirements.txt` from
the repository root. That pulls in
[machine-data-model](https://github.com/glacier-project/machine-data-model),
[frost-planner](https://github.com/glacier-project/frost-planner) and `fmpy`.

## Licence

Frost is released under the BSD 2-Clause licence.
