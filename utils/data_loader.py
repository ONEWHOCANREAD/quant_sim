import yfinance as yf
import pandas as pd

def get_historical_data(ticker: str, period: str = "5y", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch historical data for the given asset ticker using yfinance.

    Args:
        ticker (str): Asset ticker symbol (e.g., AAPL, BTC-USD)
        period (str): Time period to fetch (e.g., '1y', '6mo', '5d')
        interval (str): Data interval (e.g., '1d', '1h')

    Returns:
        pd.DataFrame: DataFrame with historical OHLCV data or None if invalid
    """
    try:
        data = yf.download(ticker, period=period, interval=interval)
        if not data.empty:
            return data
        else:
            return None
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None