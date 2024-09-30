'''
We simulate the outcome if we had the algorithm trade starting at a given capital
'''

import matplotlib.pyplot as plt
from momentum_strategy import MomentumTrendStrategy

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




