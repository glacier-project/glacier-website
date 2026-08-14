# Ecosystem

GLACIER is not a single program. It is a set of libraries and applications that
share the machine data model as a common interface.

<figure class="glacier-diagram" markdown="span">
--8<-- "diagrams/ecosystem.svg"
<figcaption>How the GLACIER repositories depend on one another.</figcaption>
</figure>

## Core libraries

**[machine-data-model](https://github.com/glacier-project/machine-data-model)**
declares what a machine exposes. It is a Python library with no dependency on
Frost: a YAML file describes a tree of folders, variables and methods, and the
library turns it into an object that can be read, written, invoked and
subscribed to. Connectors map that tree onto an OPC UA server or an MQTT broker.

**[frost](https://github.com/glacier-project/frost)** turns a data model into a
component that lives in a network. It is a library of Lingua Franca reactors
providing messaging, registration, routing and periodic update delivery, so that
a machine or a control application only has to supply its own behaviour.

**[frost-planner](https://github.com/glacier-project/frost-planner)** solves
flexible job-shop scheduling problems. Frost depends on it: the `FrostScheduler`
reactor uses a `frost-planner` scheduling instance to decide which method to
invoke on which machine.

## Getting started

**[frost-template](https://github.com/glacier-project/frost-template)** is a
GitHub template with the directory layout, configuration files and a main
reactor already in place.

**[frost-playground](https://github.com/glacier-project/frost-playground)**
collects small self-contained examples — publisher/subscriber, sensor/alarm, a
stock-market toy, a production scheduler.

!!! warning "The playground tracks the released Frost, not the current one"

    `frost-playground` pins Frost as a submodule at the `main` branch, which is
    Frost v1.0.0. Its examples therefore use the v1.0.0 component names
    (`FrostMachine`, `FrostBus`, `FrostDataModel`), which were replaced on the
    current development branch. See [Versions](../reference/versions.md).

## Applications

**[ice-frost](https://github.com/glacier-project/ice-frost)** models the
production line of the [ICE laboratory](https://www.icelab.di.univr.it/) in
Verona. Each machine extends `FrostReactor`; a `Scheduler` reads a recipe from
YAML, turns it into Frost messages, and waits for the expected responses before
advancing.

**[xppu-frost](https://github.com/glacier-project/xppu-frost)** is a digital
twin of the Extended Pick&Place Unit, a widely used Industry 4.0 research
demonstrator. It models a stack, a crane, a stamp and several conveyors, and
includes physics-based variants of some components.

**[virtualice-image](https://github.com/glacier-project/virtualice-image)**
packages the ICE laboratory's data-collection architecture — Kafka, RabbitMQ and
supporting services — as a Docker Compose deployment.

## Full listing

The [Repositories](../reference/repositories.md) page lists every public GLACIER
repository with its purpose, default branch and licence.
