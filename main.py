from momentum_strategy import MomentumTrendStrategy, optimize_parameters
from simulate_trading import SimulatedTradingStrategy


# Define the asset and time period
symbol = 'AAPL'  # Apple Inc.
# Simulation period
start_date = '2023-01-01'
end_date = '2024-04-29'
initial_capital = float(1000)  # Starting with $100

# Optimization period
opt_start_date = '2021-01-01'
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