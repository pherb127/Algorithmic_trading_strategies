'''
Purpose :
The goal of this project is to familiarize myself with Algorithmic Trading by implementing myself 
the momentum strategy in quantitative trading. This project was mainly inspired by this existing github project :
 https://github.com/cengizozel/Algorithmic-Trading-In-Python/blob/main/Projects/2%20-%20Building%20A%20Quantitative%20Momentum%20Investing%20Strategy/002_quantitative_momentum_strategy.ipynb,
and many other online sources, but note that much liberty was taken while implementing the code ! 
Have fun and if you have any question do not hesitate to reach out!

Prerequisites :
Python Version: Ensure you have Python 3.7 or higher installed.
Virtual Environment: It's recommended to use a virtual environment to manage dependencies.
Libraries : you will also need seaborn, quantstats and ta libraries

Explanation of the momentum strategy : 
The momentum trading strategy is a popular approach in financial markets where traders aim to capitalize
 on the continuance of existing trends in asset prices. The fundamental idea is that assets which have been increasing 
 in price are likely to continue rising, and those decreasing are likely to continue falling. 
 This strategy leverages market psychology and herd behavior, exploiting the tendency of investors to follow the majority.



Appendix :
Momentum : Momentum in trading refers to the rate at which the price of an asset is moving in a particular direction.
           It is based on the concept that price movements can persist in one direction for a significant period due to 
           investor behavior and market dynamics.

RSI : The Relative Strength Index (RSI) is a popular momentum oscillator used in technical analysis to measure the speed and
      change of price movements of an asset. It oscillates between 0 and 100 and is used to identify overbought or oversold 
      conditions in the market.
        * Overbought Condition: When the RSI value is above 70, it suggests that the asset may be overbought and could be due for a price correction downward.
        * Oversold Condition : When the RSI value is below 30, it indicates that the asset may be oversold and could be due for a price rebound upward.
      In the context of the Momentum-Based Trend Following strategy, the RSI helps confirm the strength of a trend and filters out potential false signals.
        
MA : A Moving Average (MA) is a technical analysis tool that averages a security's price over a specified time frame, 
     which can be adjusted to suit the trader's preference. As new price data becomes available, the average moves forward, 
     hence the term "moving" average. They are used to :
       * Identify Trends: Determine the direction and strength of a trend.
       * Generate Signals: Provide buy or sell signals when moving averages cross over.
     A Simple Moving Average (SMA) is easily computed bu take the Price of the asset during a time range i divided by the number of periods.

Documentation :
    ta.momentum/trend : https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html

'''

import quantstats as qs  


import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import quantstats as qs
from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator
import seaborn as sns

class MomentumTrendStrategy:
    def __init__(self, symbol, start_date, end_date, sma_short=50, sma_long=200, rsi_period=14, rsi_upper=70, rsi_lower=30):
        self.symbol = symbol
        self.sma_short = sma_short
        self.sma_long = sma_long
        self.rsi_period = rsi_period
        self.rsi_upper = rsi_upper
        self.rsi_lower = rsi_lower
        self.data = self.get_data(start_date, end_date)
        self.prepare_data()
    
    def get_data(self, start_date, end_date):
        data = yf.download(self.symbol, start=start_date, end=end_date)
        return data
    
    def prepare_data(self):
        # Calculate Moving Averages
        self.data['SMA_short'] = SMAIndicator(self.data['Close'], window=self.sma_short).sma_indicator()
        self.data['SMA_long'] = SMAIndicator(self.data['Close'], window=self.sma_long).sma_indicator()
        
        # Calculate RSI
        self.data['RSI'] = RSIIndicator(self.data['Close'], window=self.rsi_period).rsi()
        
        # Generate Signals
        self.generate_signals()
    
    def generate_signals(self):
        self.data['Position'] = 0  # Default to no position

        # Define entry conditions
        long_condition = (
            (self.data['SMA_short'] > self.data['SMA_long']) &
            (self.data['RSI'] > 50) & (self.data['RSI'] < self.rsi_upper)
        )
        short_condition = (
            (self.data['SMA_short'] < self.data['SMA_long']) &
            (self.data['RSI'] < 50) & (self.data['RSI'] > self.rsi_lower)
        )

        # Set positions
        self.data.loc[long_condition, 'Position'] = 1  # Long
        self.data.loc[short_condition, 'Position'] = -1  # Short

        # Calculate daily returns
        self.data['Market_Returns'] = self.data['Close'].pct_change()
        self.data['Strategy_Returns'] = self.data['Market_Returns'] * self.data['Position'].shift(1)
    
    def backtest(self, transaction_cost=0.0001):
        # Apply transaction costs
        trades = self.data['Position'].diff().abs()
        self.data['Strategy_Returns'] = self.data['Strategy_Returns'] - (trades * transaction_cost)
        # Calculate cumulative returns
        self.data['Cumulative_Market_Returns'] = (1 + self.data['Market_Returns']).cumprod()
        self.data['Cumulative_Strategy_Returns'] = (1 + self.data['Strategy_Returns']).cumprod()
    
    def get_performance_metrics(self):
        returns = self.data['Strategy_Returns'].dropna()
        qs.reports.full(returns)
    
    def plot_equity_curve(self):
        plt.figure(figsize=(14,7))
        plt.plot(self.data['Cumulative_Market_Returns'], label='Market Returns')
        plt.plot(self.data['Cumulative_Strategy_Returns'], label='Strategy Returns')
        plt.legend()
        plt.title(f'Equity Curve for {self.symbol}')
        plt.show()
    
    def plot_drawdowns(self):
        returns = self.data['Strategy_Returns'].dropna()
        qs.plots.drawdown(returns)


if __name__ == "__main__":
    # Define the asset and time period
    symbol = 'AAPL'  # Apple Inc.
    start_date = '2015-01-01'
    end_date = '2023-01-01'

    # Instantiate the strategy
    strategy = MomentumTrendStrategy(symbol, start_date, end_date)

    # Run backtest
    strategy.backtest()

    # Get performance metrics and plots
    strategy.get_performance_metrics()
    strategy.plot_equity_curve()
    strategy.plot_drawdowns()


def optimize_parameters(symbol, start_date, end_date):
    results = []
    sma_short_range = range(10, 60, 10) 
    sma_long_range = range(100, 250, 50)
    rsi_upper_range = range(65, 85, 5)
    rsi_lower_range = range(15, 35, 5)

    for sma_short in sma_short_range:
        for sma_long in sma_long_range:
            if sma_short >= sma_long:
                continue  # Short SMA should be less than Long SMA
            for rsi_upper in rsi_upper_range:
                for rsi_lower in rsi_lower_range:
                    if rsi_lower >= rsi_upper:
                        continue  # Lower RSI threshold should be less than upper
                    strategy = MomentumTrendStrategy(
                        symbol, start_date, end_date,
                        sma_short=sma_short,
                        sma_long=sma_long,
                        rsi_upper=rsi_upper,
                        rsi_lower=rsi_lower
                    )
                    strategy.backtest()
                    total_return = strategy.data['Cumulative_Strategy_Returns'][-1] - 1
                    results.append({
                        'sma_short': sma_short,
                        'sma_long': sma_long,
                        'rsi_upper': rsi_upper,
                        'rsi_lower': rsi_lower,
                        'total_return': total_return
                    })
    # Convert results to DataFrame
    results_df = pd.DataFrame(results)
    # Find the best parameters
    best_result = results_df.loc[results_df['total_return'].idxmax()]
    print("Best Parameters:")
    print(best_result)
    return results_df


if __name__ == "__main__":
    # Optimize parameters
    results_df = optimize_parameters(symbol, start_date, end_date)

def plot_optimization_results(results_df):
    pivot_table = results_df.pivot_table(values='total_return', index='sma_short', columns='sma_long', aggfunc='max')
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_table * 100, annot=True, fmt=".2f", cmap='viridis')
    plt.title('Total Return Heatmap for SMA Parameters (%)')
    plt.ylabel('SMA Short Period')
    plt.xlabel('SMA Long Period')
    plt.show()

if __name__ == "__main__":
    # Plot optimization results
    plot_optimization_results(results_df)


if __name__ == "__main__":
    # Extract best parameters
    best_params = results_df.loc[results_df['total_return'].idxmax()]
    sma_short = int(best_params['sma_short'])
    sma_long = int(best_params['sma_long'])
    rsi_upper = int(best_params['rsi_upper'])
    rsi_lower = int(best_params['rsi_lower'])

    # Run backtest with best parameters
    strategy = MomentumTrendStrategy(
        symbol, start_date, end_date,
        sma_short=sma_short,
        sma_long=sma_long,
        rsi_upper=rsi_upper,
        rsi_lower=rsi_lower
    )
    strategy.backtest()
    strategy.get_performance_metrics()
    strategy.plot_equity_curve()
    strategy.plot_drawdowns()


