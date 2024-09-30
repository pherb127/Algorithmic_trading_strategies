import quantstats as qs  
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import quantstats as qs
from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator
import seaborn as sns
from momentum_strategy import MomentumTrendStrategy, optimize_parameters, plot_optimization_results


# Define the asset and time period
symbol = 'AAPL'  # Apple Inc.
start_date = '2015-01-01'
end_date = '2024-09-30'

# Instantiate the strategy
strategy = MomentumTrendStrategy(symbol, start_date, end_date)

# Run backtest
strategy.backtest()

# Get performance metrics and plots
strategy.get_performance_metrics()
strategy.plot_equity_curve()
strategy.plot_drawdowns()

# Optimize parameters
results_df, best_params = optimize_parameters(symbol, start_date, end_date)
plot_optimization_results(results_df)

# Extract best parameters
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
