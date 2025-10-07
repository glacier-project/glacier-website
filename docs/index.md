

# **The GLACIER Project**
<!---
!!! warning 
    The GLACIER platform is under active development. The documentation is a work in progress and may contain errors or incomplete information.
-->
## Overview

The GLACIER project aims to create an open-source ecosystem for designing, prototyping, monitoring, and optimizing cyber-physical production systems (CPPSs).
With steadily increasing complexity of manufacturing systems and the integration of software in manufacturing systems, the need for tools supporting the design, prototyping, monitoring, and optimization of production systems has become more important. 

The GLACIER ecosystem provides a simplified environment for developing CPPSs Digital Twins (DTs), where software and physical components are seamlessly integrated. 
Physical components represent the real-world manufacturing machines, sensors, and actuators, while software components represent the software controlling, monitoring, and optimizing the production system. 
GLACIER supports different levels of fidelity, from simple data-mirroring models to complex predictive simulations. The architecture is designed to be modular, scalable, and extensible.
This flexibility allows users to start with basic digital representations and gradually enhance them as requirements evolve.

### [The Frost Platform](https://github.com/esd-univr/frost)

The Frost platform is the core of the GLACIER ecosystem, providing a simulation environment for developing and testing CPPSs.
Frost allows users to create high-fidelity digital twins of production systems replicating the Application Programming Interfaces (APIs) exposed by real systems.
Such an environment reduces the time spent adapting and deploying prototype software on the target system.
<!-- Figure 1 shows an example of a digital twin of a production system based on Frost. 
The digital twin mirrors the behavior of the real manufacturing plan by mimicking also the behavior of the digital infrastructure responsible for communication, synchronization, and data collection in the actual system. -->
Frost is built on [Lingua Franca](https://www.lf-lang.org/), a polyglot coordination language supporting the development of deterministic distributed programs that can be deployed on the Cloud, the Edge, and even on bare-metal architectures.
This combination makes it ideal for enhancing the reliability of software prototyping and testing.
At its core, the Frost platform follows a modular architecture with several key components:

- **Data Model**: the interface between the machine and the other components of the platform. Inspired by the OPC UA Information model, it consists of a tree-like structure containing the variables that represent the state of the machine, and the methods that represents the exposed functionalities. 
- **FrostMachine**: physical components of the production system, such as machines, sensors, and actuators. Machines can be represented with different levels of fidelity, from simple delay-based models to physics-based simulations.
- **Actor**: components that interact with the machines or other actors. Actors can be used to implement control algorithms, monitoring applications, or optimization algorithms. 
- **FrostBus**: the communication infrastructure of the production system, where software components and physical components interact. The bus is responsible for routing messages between components and ensuring that the system is in a consistent state.

### [Data Model](https://github.com/esd-univr/frost-machine-data-model) 

The machine data model is the interface between the machine and the other components of the platform. It is inspired by the OPC UA Information model and consists of a tree-like structure containing the variables that represent the state of the machine. Specifically, the data model supports the following types of variables:

- **FolderNode**: folders that contain other variables. Folders can be nested to create a tree-like structure.
- **VariableNode**: variables that represent the state of the machine. Variables can be of different types, such as integers, floats, strings, booleans, etc.
- **ObjectNode**: objects that represent complex components of the machine. Objects can contain other variables or objects.
- **MethodNode**: _synchronous_ methods that can be invoked to perform actions on the machine. Methods can accept arguments and return values. A synchronous method returns the result of the command only after the command has been successfully executed or has failed. They can be used to represent actions that are executed across multiple time steps.
- **AsyncMethodNode**: _asynchronous_ methods return immediately. The completion of the command is signaled through an update of one or more variables in the data model. They can be used to represent actions changing the state of the machine (e.g., turning on a motor).
- **CompositeMethodNode**: _composite_ methods are defined as a sequence of operations performed on the data model. The operations may include the execution of asynchronous methods, reading and writing variables, and waiting for specific conditions on the data model. When a composite method is invoked, it returns immediately, returning an acceptance value, while when it is completed, an update message is sent to the caller. 

The data model is specified in a YAML file that describes the structure of the tree and the variables that compose the model.
The following example shows a data model for a production machine that checks the quality of a product.

```yaml title="control_quality.yaml" linenums="1"
name: "control_quality" # name of the machine
description: "A simple quality control machine" # description of the machine
root:
  !!FolderNode
  name: "control_quality"
  description: "Root folder of the control quality machine"
  children:
    - !!FolderNode
      name: "statistics"
      description: "Statistics folder"
      children:
        - !!NumericalVariableNode
            name: "#checks"
            description: "Total number of checks"
            initial_value: 0
        - !!NumericalVariableNode
            name: "failures"
            description: "Number of failed checks"
            initial_value: 5.0
        - !!AsyncMethodNode
          name: "check_quality"
          description: "Check the quality of a product"
          parameters:
            - !!StringVariableNode
              name: "product_info"
              description: "Information about the product"
              default_value: "default"
          returns:
            - !!BooleanVariableNode
              name: "result"
              description: "Result of the quality check"
```

### Frost Machines 

In the Frost platform, machines are the physical components of the production system.
Each machine is represented as a single entity, which can be a physical machine, a sensor, or an actuator.
Interactions with a machine occur through the machine's data model, which represents the current state of the machine.
This enables decoupling the execution logic of the machine from that of other components, increasing the modularity and flexibility of the platform. To create a new machine, you need to extend the base reactor `FrostMachine` and implement the necessary methods for the simulation or control of the machine.

```lf-python title="ControlQuality.lf" linenums="1"
reactor ControlQuality extends FrostMachine{
    state total_checks
    state failures

    reaction(startup){=
        self.total_checks = self.data_model.get_node("control_quality/statistics/#checks")
        self.failures = self.data_model.get_node("control_quality/statistics/failures")
        check_quality_covers = self.data_model.get_node("control_quality/statistics/check_quality")
        check_quality_covers.callback = self.check_quality
    =}

    method check_quality(product_info){=
        self.total_checks.value += 1
        
        if product_info != "good":
            self.failures.value += 1
            return False
        return True
    =}
}
```
<!-- !!! note 
    Check if a LF formatter is available for the code snippet above. -->

The example above shows a simple implementation of a quality control machine that checks the quality of a product. The machine references the data model presented above, adding the necessary logic implementing the machine behavior.
The state of the machine is represented by the `total_checks` and `failures` variables, which are initialized at startup. These variables reference the corresponding variables in the data model. Changes to the state of these variables are transparently handled by the machine data model and the `FrostMachine` base class.

### Actor

Actors are software components that interact with machines or other actors.
They can be used to implement control algorithms, monitoring applications, or optimization algorithms.
Actors interact with machines or with other actors by reading and writing variables in the machine data model, invoking methods on the machine, or subscribing to changes in the data model's state.

<!-- !!! warning
    Add here a small example of an actor that interacts with a machine. -->

### Frost Bus

Modern manufacturing systems follows the Service-oriented Manufacturing (SoM) paradigm, which organizes the system as a set of *machine services* that can be accessed and used by other entities in the system.
The implementation of the SoM paradigm is usually based on a centralized message broker that routes messages between the different components of the system. 
To emulate this behavior, the Frost platform includes a bus component that serves as a communication infrastructure for the system.
The bus component is responsible for routing messages between machines and actors, ensuring that the system is in a consistent state.

!!! note
    The bus component is optional and can be replaced by direct communication between actors and machines for brokerless architectures.

<!-- !!! warning
    Add here a small description of the Bus component. -->

### Wrapping Up

Below is a simple example of a production system that includes a quality control machine and an actor that interacts with the machine. The actor invokes the `check_quality` method to check the quality of a product and prints the result of the check. The machine keeps track of the total number of checks and the number of failed checks.

```lf-python title="ControlQualityActor.lf" linenums="1"
target Python{
    fast: True,
}

import ControlQuality from "ControlQuality.lf"
import FrostBus from "FrostBus.lf"

reactor ControlQualityActor extends FrostMachine{

    reaction(startup) -> channel_out{=
        # send a message to the machine to check the quality of a product
        msg = get_cm_msg(target="qc", method_name="control_quality/statistics/check_quality", args=["good"])
        # alternatively, you can specify the arguments as a dictionary
        # msg = get_cm_msg(target="qc", method_name="control_quality/statistics/check_quality", kwargs={"product_info": "good"})

        channel_out.set(msg)
    =}

    reaction(channel_in){=
        print("Received message: ", self.channel_in.value)
    =}
}

main reactor{
    qc_actor = new ControlQualityActor()
    qc = new ControlQuality(model_path="models/control_quality.yml")
    bus = new FrostBus(model_path="models/bus.yml",width=2)

    qc_actor.channel_out, qc.channel_out -> bus.channel_in 
    bus.channel_out -> qc.channel_in, qc_actor.channel_in 
}
```


---
## Roadmap

The GLACIER ecosystem is under active development. The following roadmap outlines the key milestones and features that will be added to the platform in the coming months.

``` mermaid
timeline
    title GLACIER Roadmap
    2025-03-31: First release
    2025-04-30: SysML v2 integration: Data-driven machine simulation
    2025-05-31: Physic-based machine simulation: Machine-in the loop simulation
    2025-07-31: FMI/FMU integration
    2025-12-31: Verification, validation, and testing
    2026-03-31: Advanced Human-Machine Interaction
```

## License 

The [Frost platform](https://github.com/esd-univr/frost) and the [data model library](https://github.com/esd-univr/frost-machine-data-model) are released under the BSD 2-Clause License.

## Contact

For technical support, collaborations, or further information, contact:

Sebastiano Gaiardelli (sebastiano.gaiardelli@univr.it), Department of Engineering for Innovation Medicine University of Verona, Section of Engineering and Physics, Italy