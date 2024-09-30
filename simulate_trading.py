'''
We simulate the outcome if we had the algorithm trade starting at 100$ initial capital
'''


import matplotlib.pyplot as plt
from momentum_strategy import MomentumTrendStrategy, optimize_parameters

class SimulatedTradingStrategy(MomentumTrendStrategy):
    def __init__(self, symbol, start_date, end_date, initial_capital=100, **kwargs):
        super().__init__(symbol, start_date, end_date, **kwargs)
        self.initial_capital = initial_capital

    
    def simulate_trading(self, transaction_cost=0.0001):
        self.data['Portfolio_Value'] = float(self.initial_capital)
        self.data['Holdings'] = 0  # Number of shares held
        self.data['Cash'] = self.initial_capital  # Cash in hand

        for i in range(1, len(self.data)):
            position_change = self.data['Position'].iloc[i] - self.data['Position'].iloc[i-1]
            price = self.data['Close'].iloc[i]
            if position_change == 1:
                # Enter long position
                shares_to_buy = float((self.data['Cash'].iloc[i-1] * 0.99) / price)  # Use 99% of cash
                cost = shares_to_buy * price
                self.data.at[self.data.index[i], 'Holdings'] = shares_to_buy
                self.data.at[self.data.index[i], 'Cash'] = self.data['Cash'].iloc[i-1] - cost - (cost * transaction_cost)
            elif position_change == -1:
                # Exit long position
                proceeds = self.data['Holdings'].iloc[i-1] * price
                self.data.at[self.data.index[i], 'Holdings'] = 0
                self.data.at[self.data.index[i], 'Cash'] = self.data['Cash'].iloc[i-1] + proceeds - (proceeds * transaction_cost)
            else:
                # Hold position
                self.data.at[self.data.index[i], 'Holdings'] = self.data['Holdings'].iloc[i-1]
                self.data.at[self.data.index[i], 'Cash'] = self.data['Cash'].iloc[i-1]

            # Update portfolio value
            holdings_value = float(self.data['Holdings'].iloc[i] * price)
            self.data.at[self.data.index[i], 'Portfolio_Value'] = holdings_value + self.data['Cash'].iloc[i]

        # Plot portfolio value over time
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['Portfolio_Value'], label='Portfolio Value')
        plt.title(f"Portfolio Value Over Time for {self.symbol}")
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value ($)')
        plt.legend()
        plt.show()

        # Print final portfolio value
        final_value = self.data['Portfolio_Value'].iloc[-1]
        print(f"Final Portfolio Value: ${final_value:.2f}")
        print(f"Total Return: {(final_value - self.initial_capital) / self.initial_capital * 100:.2f}%")



# Define the asset and time period
symbol = 'AAPL'  # Apple Inc.
# Simulation period
start_date = '2021-01-01'
end_date = '2024-09-29'
initial_capital = float(100)  # Starting with $100

# Optimization period
opt_start_date = '2015-01-01'
opt_end_date = '2024-9-29'

# Perform optimization to get optimal parameters
results_df, best_params = optimize_parameters(symbol, opt_start_date, opt_end_date)

# Extract optimal parameters
optimal_params = {
    'sma_short': int(best_params['sma_short']),
    'sma_long': int(best_params['sma_long']),
    'rsi_period': 14,  # Adjust if you have optimized this
    'rsi_upper': int(best_params['rsi_upper']),
    'rsi_lower': int(best_params['rsi_lower'])
}

# Instantiate the simulated trading strategy with optimal parameters
strategy = SimulatedTradingStrategy(
    symbol, start_date, end_date,
    initial_capital=initial_capital,
    **optimal_params
)

# Run simulation
strategy.simulate_trading()

