---
hide:
  - navigation
  - toc
---

<div class="glacier-hero" markdown>

# Open tools for cyber-physical production systems

GLACIER is an open-source ecosystem from the University of Verona for
modelling, simulating and validating the software that controls manufacturing
systems. Build a virtual version of a production line, develop the control
software against it, and test it before it ever touches the plant.

[Explore GLACIER](overview/index.md){ .md-button .md-button--primary }
[Frost documentation](frost/index.md){ .md-button }
[Learn GLACIER](learn/index.md){ .md-button }

</div>

## Where to go next

<div class="grid cards" markdown>

-   __Overview__

    ---

    What GLACIER is, the problem it addresses, and how its pieces fit
    together.

    [:octicons-arrow-right-24: Read the overview](overview/index.md)

-   __Frost__

    ---

    The simulation and control framework at the centre of GLACIER: its
    reactors, its data model, and worked examples.

    [:octicons-arrow-right-24: Frost documentation](frost/index.md)

-   __Learn__

    ---

    Tutorials, hands-on labs and lecture material that use GLACIER tools.

    [:octicons-arrow-right-24: Learning resources](learn/index.md)

-   __Repositories__

    ---

    The public GLACIER repositories, what each one is for, and how they
    relate.

    [:octicons-arrow-right-24: Browse the repositories](reference/repositories.md)

</div>

## What GLACIER gives you

**A machine interface you can describe once.** Machines expose their state and
their operations through a data model — a tree of variables and methods
declared in YAML, inspired by the OPC UA information model. Control software
talks to that interface, not to a particular machine implementation.

**A deterministic execution model.** Frost is built on
[Lingua Franca](https://www.lf-lang.org/), a coordination language whose
reactors execute deterministically under a logical clock. Repeating a Frost
simulation with the same inputs gives the same interleaving of events.

**A path from simulation towards hardware.** The same data model can be backed
by a simulated machine or, through a connector, by a real OPC UA server or MQTT
broker. Frost is designed so that control software written against a simulated
plant needs few or no changes when the interface is pointed at real equipment.

!!! note "Where this documentation stands"

    GLACIER is a research project under active development. These pages
    document the current development branches of the GLACIER repositories, and
    say so explicitly wherever the released versions differ. See
    [Versions](reference/versions.md).
