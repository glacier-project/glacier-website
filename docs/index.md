# The GLACIER Platform  

!!! warning 
    The GLACIER platform is under active development. The documentation is a work in progress and may contain errors or incomplete information.

## Overview

The GLACIER platform is am open-source ecosystem for designing, prototyping, monitoring, and optimizing cyber-physical production systems (CPPSs).
With steadily increasing complexity of manufacturing systems and the integration of software in manufacturing systems, the need for tools supporting the design, prototyping, monitoring, and optimization of production systems has become more important. 

The GLACIER platform provides a simplified environment for developing Digital Twins (DTs) of CPPSs, where software and physical components are seamlessly integrated. 
Physical components represent the real-world manufacturing machines, sensors, and actuators, while software components represent the software controlling, monitoring, and optimizing the production system. 
GLACIER supports different levels of fidelity, from simple data-mirroring models to complex predictive simulations. The architecture is designed to be modular, scalable, and extensible.
This flexibility allows users to start with basic digital representations and gradually enhance them as requirements evolve.
GLACIER's architecture is built on [Lingua Franca](https://www.lf-lang.org/), a polyglot coordination language for developing distributed programs that can be deployable on the Cloud, the Edge and even on bare-metal architectures. 
As its core, the platform follows a modular architecture with several key components:

- **Machine Data Model**: the interface between the machine and the other components of the platform. Inspired by the OPC UA Information model, it consists of a tree-like structure containing the variables that represent the state of the machine. 
- **Machine**: physical components of the production system, such as machines, sensors, and actuators. Machines can be represented with different levels of fidelity, from simple delay-based models to physics-based simulations.
- **Actor**: components that interact with the machines or other actors. Actors can be used to implement control algorithms, monitoring applications, or optimization algorithms. 
- **Bus**: the communication infrastructure of the production system, where software components and physical components interact. The bus is responsible for routing messages between components and ensuring that the system is in a consistent state.

!!! note
    The Bus component is optional and can be replaced by direct communication between actors and machines for distributed systems with low latency requirements. 

### Machine Data Model 

The machine data model is the interface between the machine and the other components of the platform. It is inspired by the OPC UA Information model and consists of a tree-like structure containing the variables that represent the state of the machine. Specifically, the data model supports the following types of variables:

- **FolderNode**: folders that contain other variables. Folders can be nested to create a tree-like structure.
- **VariableNode**: variables that represent the state of the machine. Variables can be of different types, such as integers, floats, strings, booleans, etc.
- **ObjectNode**: objects that represent complex components of the machine. Objects can contain other variables or objects.
- **MethodNode**: _synchronous_ methods that can be invoked to perform actions on the machine. Methods can accept arguments and return values. A synchronous method returns the result of the command only after the command has been successfully executed or has failed. They can be used to represent actions that are executed across multiple time steps.
- **AsyncMethodNode**: _asynchronous_ methods return immediately. The completion of the command is signaled through an update of one or more variables in the data model. They can be used to represent actions changing the state of the machine (e.g., turning on a motor).
- **CompositeMethodNode**: _composite_ methods are defined as a sequence of operations performed on the data model. The operations may include the execution of asynchronous methods, reading and writing variables, and waiting for specific conditions on the data model. When a composite method is invoked, it returns immediately returning an acceptance value. When the method is completed, a message is sent to the caller. 

The data model is specified in a YAML file that describes the structure of the tree and the variables that compose the model.
The following example shows a data model for a production machine that checks the quality of a product.

```yaml title="control_quality.yaml"
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
            value: 0
        - !!NumericalVariableNode
            name: "failures"
            description: "Number of failed checks"
            value: 0
        - !!AsyncMethodNode
          name: "check_quality"
          description: "Check the quality of a product"
          parameters:
            - !!StringVariableNode
              name: "product_info"
              description: "Information about the product"
          returns:
            - !!BooleanVariableNode
              name: "result"
              description: "Result of the quality check"
```

### Machine 

!!! warning
    The description of the GlacierMachine should be added here. With the description of the Read, Write, Subscribe and Method invocation.

In the GLACIER ecosystem, a machine is a physical component of the production system. 
Each machine is represented as a single entity within the system. 
Interactions with a machine occur through the machine's data model, which represents the current state of the machine.
This enables decoupling the execution logic of the machine from that of other components, increasing the modularity and flexibility of the platform. To create a new machine, you need to extend the base reactor `GlacierMachine` and implement the necessary methods for the simulation or control of the machine.

```python title="ControlQuality.lf"
reactor ControlQuality extends GlacierMachine{
    state total_checks
    state failures

    reaction(startup){=
        self.total_checks = self.data_model.get_node("control_quality/statistics/#checks")
        self.failures = self.data_model.get_node("control_quality/statistics/failures")
    =}

    method check_quality(product_info){=
        self.num_total_checks.value += 1
        
        if product_info != "good":
            self.failures.value += 1
            return False
        return True
    =}
}
```
!!! note 
    Check if a LF formatter is available for the code snippet above.

This example shows a simple implementation of a quality control machine that checks the quality of a product. The machine references the data model presented above, adding the necessary logic implementing the machine behavior. 
The state of the machine is represented by the `total_checks` and `failures` variables, which are initialized at startup. These variables reference the corresponding variables in the data model. Changes to the state of these variables are transparently handled by the machine data model and the `GlacierMachine` base class.

### Actor

Actors are software components that interact with machines or other actors.
They can be used to implement control algorithms, monitoring applications, or optimization algorithms.
Actors interact with machines or with other actors by reading and writing variables in the machine data model, invoking methods on the machine, or subscribing to changes in the data model's state.

!!! warning
    Add here a small example of an actor that interacts with a machine.

### Bus

!!! warning
    Add here a small description of the Bus component.

### A Simple Example

!!! warning
    Here we should add a simple example of a production system with few machine, the bus and a simple actor.

## Roadmap

The GLACIER platform is under active development. The following roadmap outlines the key milestones and features that will be added to the platform in the coming months.
For more information, please follow the [GLACIER GitHub repository](https://github.com/esd-univr/glacier).

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

