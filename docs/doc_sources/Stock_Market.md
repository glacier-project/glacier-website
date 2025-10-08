# Stock Market Simulation

This example demonstrates a simple stock market simulation with Frost components. The simulation features two main components: a `Stock_Market` reactor that simulates fluctuating stock prices and an `Investor` reactor that makes trading decisions based on market trends.

### The `StockMarket` Data Model

The simulation starts with a data model that defines the initial state of the stocks. This model is defined in a YAML file and loaded by the `Stock_Market` reactor at startup. It establishes the initial values for three stocks: `action_1`, `action_2`, and `action_3`.

```yaml
name: "stock_market"
machine_category: "unknown"
machine_type: "unknown"
machine_model: "unknown"
description: "Stock Market"
root:
  !!FolderNode
  name: "root"
  description: "none"
  children:
    - !!NumericalVariableNode
      name: "action_1"
      initial_value: 27.5
    - !!NumericalVariableNode
      name: "action_2"
      initial_value: 50.0
    - !!NumericalVariableNode
      name: "action_3"
      initial_value: 12.5
```

### The `Stock_Market` Reactor

The `Stock_Market` reactor is responsible for emulating the dynamic behavior of the stock market with a random change of the action values. At startup, it loads the initial stock values from the data model. It then uses a timer to periodically update the values of the stocks, introducing random fluctuations to simulate market volatility. This reactor essentially serves as the "environment" for our simulation.

```lf-python
reactor Stock_Market extends FrostDataModel {
    state action_1
    state action_2
    state action_3

    timer update_timer(1 sec, 100 msec)
    reaction(update_timer) {=
        // Randomly update stock values, ensuring they don't go below zero
         change1 = random.choice([-1, 1])
        if self.action_1.value + change1 > 0:
            self.action_1.value += change1
        change2 = random.choice([-2, 2])
        if self.action_2.value + change2 > 0:
            self.action_2.value += change2
        change3 = random.choice([-3, 3])
        if self.action_3.value + change3 > 0:
            self.action_3.value += change3
    =}
}
```

### The `Investor` Reactor

The `Investor` reactor acts as an autonomous agent that implements a simple trading strategy. It periodically sends requests to the `Stock_Market` reactor to get the current stock prices. Based on the received values, it decides whether to buy or sell stocks.

- **Buying Strategy**: If a stock's price falls below a predefined `threshold`, the investor sees a buying opportunity and purchases a number of shares. The quantity is determined by how far the price is below the threshold.
- **Selling Strategy**: If a stock's price rises above the `threshold`, the investor sells its holdings of that stock to realize a profit.

This reactor demonstrates how to model agent-like behavior and decision-making logic in Lingua Franca.

```lf-python
reactor Investor extends FrostBase {
    input channel_in
    output channel_out
    state threshold = 20.0
    state money = 1000.0

    reaction(channel_in) {=
        // ... receive message and extract stock value ...
        percentage = float(value / self.threshold) * 100.0
        if percentage > 100.0 and self.action_1 > 0:
            // Sell stock
            self.money += value * self.action_1
            self.action_1 = 0
        elif percentage < 100.0:
            // Buy stock if there is enough money
            num_to_buy = int(100 - percentage)
            cost = num_to_buy * value
            if cost < self.money:
                self.action_1 += num_to_buy
                self.money -= cost
    =}
}
```

### The `main` Reactor

The `main` reactor is the top-level component that assembles the simulation. It instantiates both the `Stock_Market` and `Investor` reactors and establishes the communication channels between them. This connection creates a closed loop: the `Investor` requests data from the `Stock_Market`, which in turn provides the data that drives the `Investor`'s decisions.

```lf-python
main reactor {
    stock_market_action = new Stock_Market(name = "stock_market")
    investor = new Investor(name = "investor")

    stock_market_action.channel_out -> investor.channel_in after 0
    investor.channel_out -> stock_market_action.channel_in after 0
}
```