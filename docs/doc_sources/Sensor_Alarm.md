# Sensor-Alarm Example

This example demonstrates a fundamental event-driven interaction between a `Sensor` and an `Alarm`. The `Sensor` reactor is designed to periodically monitor for a specific condition. If the condition is met, it triggers an event by sending a message to the `Alarm` reactor, which then takes appropriate action. 

### The Data Models

The simulation is defined by two simple data models, one for the sensor and one for the alarm, which specify their respective states.

**Sensor Data Model (`sensor.yml`)**

The sensor's data model contains a single boolean node called `detected`. This node represents whether the sensor has detected the event it is monitoring. It is initialized to `False`.

```yaml
name: "sensor"
description: "Sensor"
root:
  !!FolderNode
  name: "root"
  children:
    - !!BooleanVariableNode
      name: "detected"
      initial_value: False
```

**Alarm Data Model (`alarm.yml`)**

The alarm's data model includes a boolean node called `ringing`, which is also initialized to `False`. This node represents the state of the alarm. The `Alarm` reactor will set this to `True` when it receives a signal from the sensor.

```yaml
name: "alarm"
description: "Alarm"
root:
  !!FolderNode
  name: "root"
  children:
    - !!BooleanVariableNode
      name: "ringing"
      initial_value: False
```

### The `Sensor` Reactor

The `Sensor` reactor simulates the behavior of a real-world sensor. It uses a timer to periodically perform a check. In this simulation, the check involves generating a random number. If this number exceeds a predefined threshold, the sensor considers the event "detected," sets its `detected` state to `True`, and sends a message to the `Alarm` reactor to activate it.

```lf-python
reactor Sensor extends FrostMachine {
    state detected

    reaction(startup) {=
        self.detected = self.data_model.get_node("root/detected")
    =}

    timer check_timer(1000 msec, 3000 msec)

    reaction(check_timer) -> channel_out {=
        // Simulate random detection
        new_value = random.random()
        self.detected.value = new_value > 0.9

        if self.detected.value:
            message = FrostMessage(
                sender=self.name,
                target="alarm",
                // ... message header ...
                payload=VariablePayload(
                    node="root/ringing",
                    value=self.detected.value,
                ),
            )
            self._set_channel_out_port(message, channel_out)
    =}
}
```

### The `Alarm` Reactor

The `Alarm` reactor represents the alarm device itself. It has a `ringing` state that is initially `False`. The `Alarm` reactor also has a timer that periodically checks the value of its `ringing` state. If it finds that `ringing` is `True`, it logs a "RINGING!" message to the console and requests the simulation to stop. This shows how a component can react to an event triggered by another component and take a decisive action.

```lf-python
reactor Alarm extends FrostMachine {
    state ringing

    reaction(startup) {=
        self.ringing = self.data_model.get_node("root/ringing")
    =}

    timer check_status(1 sec, 1 sec)

    reaction(check_status) {=
        if self.ringing.value:
            self.logger.error("Alarm is RINGING!")
            lf.request_stop()
    =}
}
```

```lf-python
main reactor {
    frost_bus = new FrostBus(name = "frost_bus", width = 2)
    sensor = new Sensor(name = "sensor")
    alarm = new Alarm(name = "alarm")

    frost_bus.channel_out -> sensor.channel_in, alarm.channel_in after 10 msec
    sensor.channel_out, alarm.channel_out -> frost_bus.channel_in after 10 msec
}
```
