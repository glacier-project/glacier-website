# What is GLACIER?

GLACIER is an open-source ecosystem for designing, prototyping, monitoring and
optimising **cyber-physical production systems** (CPPSs). It is developed at the
Department of Engineering for Innovation Medicine of the University of Verona.

## The problem

Software is now a large part of what a manufacturing system *is*. A production
line is a collection of machines, sensors and actuators, coordinated by control
software that schedules work, reacts to sensor events and reports status
upstream.

That software is difficult to develop, for a practical reason: the machine it
controls is expensive, shared, and often not finished yet. Testing a scheduler
against a real production line means booking the line, and a mistake can damage
equipment or scrap material. So control software tends to be written late,
tested little, and debugged on the plant floor.

## The approach

GLACIER's answer is to give the control software something to talk to before
the machine is available.

Each machine is described by a **data model**: a tree of variables (its state)
and methods (its operations), declared in YAML. Control software interacts with
the machine only through that data model — reading variables, writing
variables, invoking methods and subscribing to changes.

Because the interface is explicit and declared separately from the
implementation, the thing behind it can be swapped:

- a **simulated machine**, whose behaviour is implemented in code, so the
  control software can be developed and tested offline;
- a **remote machine**, reached through a connector to an OPC UA server or an
  MQTT broker, so the same control software can be pointed at real equipment.

The simulated side is built with [Frost](../frost/index.md), which runs on
[Lingua Franca](https://www.lf-lang.org/). Lingua Franca gives Frost a
deterministic, logical-time execution model, so a scenario replays identically
run after run — which is what makes a failing test reproducible.

## What GLACIER does *not* claim

GLACIER is a research project, and it is worth being precise about the extent of
what is implemented today.

- **Fidelity is up to you.** Frost provides the interface, the messaging and the
  execution model. How faithfully a `FrostReactor` reproduces the timing and
  physics of the machine it stands for is entirely a property of the behaviour
  you write inside it. Frost does not itself supply validated physical models.
- **Determinism is about execution, not about physics.** Lingua Franca
  guarantees a deterministic ordering of events in logical time. It does not
  guarantee that a simulation matches the real machine's timing.
- **"Deploy with no changes" is a design goal, not a guarantee.** The data model
  and connector layer exist precisely to keep control software independent of
  what sits behind the interface, and the connectors for OPC UA and MQTT are
  implemented. Whether a specific application transfers unchanged depends on
  that application.

## Next

<div class="grid cards" markdown>

-   :material-sitemap: __Architecture__

    ---

    The layers of a GLACIER system and how a message travels through them.

    [:octicons-arrow-right-24: Architecture](architecture.md)

-   :material-package-variant: __Ecosystem__

    ---

    The libraries and applications that make up GLACIER.

    [:octicons-arrow-right-24: Ecosystem](ecosystem.md)

</div>
