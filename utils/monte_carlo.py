# utils/monte_carlo.py

import numpy as np
import pandas as pd
import plotly.graph_objs as go

def run_simulation(data: pd.DataFrame, days: int, num_simulations: int = 1000):
    close_prices = data['Close']
    last_price = close_prices.iloc[-1]

    # Calculate log returns
    log_returns = np.log(close_prices / close_prices.shift(1)).dropna()
    mean = log_returns.mean()
    std_dev = log_returns.std()

    # Preallocate simulation array correctly
    simulations = np.zeros((num_simulations, days))

    for i in range(num_simulations):
        prices = np.zeros(days)
        prices[0] = last_price

        for t in range(1, days):
            drift = mean - (0.5 * std_dev**2)
            shock = std_dev * np.random.normal()
            prices[t] = prices[t - 1] * np.exp(drift + shock)

        simulations[i] = prices

    final_prices = simulations[:, -1]
    return simulations, final_prices

def plot_simulations(simulations: np.ndarray):
    """
    Create Plotly figure of Monte Carlo simulations.

    Args:
        simulations (np.ndarray): Simulated price paths

    Returns:
        go.Figure: Plotly line chart
    """
    # Plotting Monte Carlo simulations
    fig = go.Figure()
    for i in range(min(1000,simulations.shape[0])):  # limit to 1000 paths for clarity
        fig.add_trace(go.Scatter(y=simulations[i],
                                 mode="lines", 
                                 line=dict(width=1), 
                                 opacity=0.5,
                                 showlegend=False))

    fig.update_layout(
        title="Monte Carlo Simulated Price Paths",
        title_font=dict(color="#003366", size=20),  # Title text color and size

        xaxis_title="Day",
        xaxis=dict(
            title_font=dict(color="#003366"),
            tickfont=dict(color="#003366")
        ),

        yaxis_title="Price",
        yaxis=dict(
            title_font=dict(color="#003366"),
            tickfont=dict(color="#003366")
        ),
        plot_bgcolor="#f7f4f3",     # pastel background
        paper_bgcolor="#f7f4f3",
        margin=dict(l=30, r=30, t=40, b=30),
        height=500,
        template="plotly_white",
    )
    return fig

