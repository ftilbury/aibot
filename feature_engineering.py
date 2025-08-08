"""
Feature engineering for forex price data.

This module transforms raw OHLCV bars into a richer set of inputs for
machine‑learning models. It computes technical indicators such as moving
averages and the Relative Strength Index (RSI). Additional indicators can
be added as required.

The output DataFrame will include the engineered features and the
corresponding target variable (price direction) suitable for training a
classifier.
"""

import pandas as pd
import numpy as np


def _compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Compute the Relative Strength Index (RSI).

    Parameters
    ----------
    series : pandas.Series
        Price series (typically the close prices).
    period : int, default 14
        Lookback period for the RSI calculation.

    Returns
    -------
    pandas.Series
        RSI values.
    """
    delta = series.diff()
    # Separate positive and negative gains
    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)
    # Use exponential moving averages for smoothing
    avg_gain = pd.Series(gain).ewm(alpha=1 / period, min_periods=period).mean()
    avg_loss = pd.Series(loss).ewm(alpha=1 / period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Generate feature columns for modelling from a raw OHLCV DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing at least the "close" column.

    Returns
    -------
    pandas.DataFrame
        DataFrame including engineered features and a binary target column
        "target" equal to 1 if the next period's return is positive, else 0.
    """
    data = df.copy()
    # Log returns
    data['return'] = np.log(data['close'] / data['close'].shift(1))
    # Moving averages
    data['sma_fast'] = data['close'].rolling(window=10).mean()
    data['sma_slow'] = data['close'].rolling(window=30).mean()
    # Difference of moving averages
    data['sma_diff'] = data['sma_fast'] - data['sma_slow']
    # RSI
    data['rsi'] = _compute_rsi(data['close'], period=14)
    # Bollinger bands width
    rolling_std = data['close'].rolling(window=20).std()
    data['bollinger_width'] = (rolling_std * 2) / data['close']
    # Drop rows with NaNs created by rolling calculations
    data.dropna(inplace=True)
    # Target: 1 if next return positive else 0
    data['target'] = (data['return'].shift(-1) > 0).astype(int)
    data.dropna(inplace=True)
    return data