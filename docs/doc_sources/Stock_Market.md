# Stock Market Simulation

This example demonstrates a simple stock market simulation where the stock market changes the actions value randomly and the investor choose whether to buy or to sell. 

### The `StockMarketAction` Reactor

The `StockMarketAction` reactor simulates the changing values of stocks. It initializes three stocks and uses a timer to randomly update their values at regular intervals, mimicking market behavior.

```lf
reactor StockMarketAction extends FrostDataModel {
    state action_1
    state action_2
    state action_3

    timer update_timer(1 sec, 100 msec)
    reaction(update_timer) {=
        // Randomly update stock values
        self.action_1.value += random.choice([-1, 1])
        self.action_2.value += random.choice([-2, 2])
        self.action_3.value += random.choice([-3, 3])
    =}
}
```

### The `Investor` Reactor

The `Investor` reactor acts as an autonomous agent that buys and sells stocks based on a simple strategy. It periodically requests stock prices and reacts to the received data.

- **Buying Strategy**: If a stock's price is below a certain threshold, the investor buys shares.
- **Selling Strategy**: If the price is high, it sells its holdings to secure a profit.

```lf
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
            // Buy stock
            num_to_buy = int(100 - percentage)
            cost = num_to_buy * value
            if cost < self.money:
                self.action_1 += num_to_buy
                self.money -= cost
    =}
}
```

### The `main` Reactor

The `main` reactor instantiates the `StockMarketAction` and `Investor` reactors and connects them. This establishes the communication loop where the investor queries the market and the market responds with price updates, driving the simulation.

```lf
main reactor {
    stock_market_action = new StockMarketAction(name = "stock_market")
    investor = new Investor(name = "investor")

    stock_market_action.channel_out -> investor.channel_in after 0
    investor.channel_out -> stock_market_action.channel_in after 0
}
```