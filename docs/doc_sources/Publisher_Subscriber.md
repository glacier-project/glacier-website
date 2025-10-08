# Publisher-Subscriber Example

This example provides a classic publisher-subscriber pattern example. In this model, a `Publisher` reactor is responsible for generating data, while a `Subscriber` reactor listens for these updates and react accordingly. 

### The Data Models

The simulation is built upon two distinct data models, one for the publisher and one for the subscriber. These models define the structure of the data that each component manages.

**Publisher Data Model (`publisher.yml`)**

The publisher's data model is straightforward, containing a single `word` node. The `Publisher` reactor will periodically update the value of this node with a new word from a predefined list.

```yaml
name: "publisher"
description: "Publisher"
root:
  !!FolderNode
  name: "root"
  children:
    - !!StringVariableNode
      name: "word"
      initial_value: ""
```

**Subscriber Data Model (`subscriber.yml`)**

The subscriber's data model contains a `sentence` node. The `Subscriber` reactor's goal is to build a sentence by concatenating the words it receives from the publisher.

```yaml
name: "subscriber"
description: "Subscriber"
root:
  !!FolderNode
  name: "root"
  children:
    - !!StringVariableNode
      name: "sentence"
      initial_value: ""
```

### The `Publisher` Reactor

The `Publisher` reactor is the source of information in this system. It is designed to periodically generate a new piece of data and publish it. The underlying Frost framework ensures that any component that has subscribed to this data is automatically notified of the update.

```lf-python
reactor Publisher extends FrostDataModel {
    state words = ["Hello", "world", "this", "is", "a", "test", "message"]
    state word_node

    reaction(startup) {=
        self.word_node = self.data_model.get_node("root/word")
    =}

    timer publish_timer(1 sec, 2 sec)

    reaction(publish_timer) {=
        if not self.words:
            lf.request_stop()
            return
        
        word = self.words.pop(0)
        self.word_node.value = word
    =}
}
```

### The `Subscriber` Reactor

The `Subscriber` reactor's function is to listen for and consume the data published by the `Publisher`. To do this, it must first express its interest by sending a subscription request. At startup, it sends a message to the `Publisher` to subscribe to the `root/word` node. From that point on, whenever the `Publisher` updates the `word` node, the `Subscriber` will receive a notification and append the new word to its `sentence` node.

```lf-python
reactor Subscriber extends FrostDataModel {  
    state sentence

    reaction(startup) -> channel_out {=
        self.sentence = self.data_model.get_node("root/sentence")
        // Send a subscription request to the publisher for "root/word"
        message = FrostMessage(
            sender=self.name,
            target="publisher",
            identifier=str(uuid.uuid4()),
            header=FrostHeader(
                type=MsgType.REQUEST,
                version=(1, 0, 0),
                namespace=MsgNamespace.VARIABLE,
                msg_name=VariableMsgName.SUBSCRIBE,
            ),
            payload=VariablePayload(node="root/word"),
        )
        self._set_output_port(message, channel_out)
    =}

    reaction(message_filter.responses) {=
        message = message_filter.responses.value[0][1]
        if message.header.namespace == MsgNamespace.VARIABLE and message.header.msg_name == VariableMsgName.UPDATE:
            self.sentence.value += " " + message.payload.value
    =}
}
```

### The `main` Reactor

The `main` reactor instantiates and connects the `Publisher` and `Subscriber` reactors. It establishes the communication channels that allow the exchange of messages between the two components.

```lf-python
main reactor {
    publisher = new Publisher(name = "publisher")
    subscriber = new Subscriber(name = "subscriber")

    publisher.channel_out -> subscriber.channel_in after 100 msec
    subscriber.channel_out -> publisher.channel_in after 100 msec
}
```
