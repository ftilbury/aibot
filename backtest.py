"""
Backtesting engine for forex trading strategies.

Given predictions from a machine‑learning model, this module calculates the
corresponding strategy returns and performance statistics. It assumes a
simple long/flat strategy: if the prediction is 1 then go long for the
next bar; if 0 then stay flat (no position). Shorting is not enabled by
default to simplify risk management, but could be added by allowing
negative positions.

Performance metrics include cumulative returns and the Sharpe ratio. You
can extend this module with additional measures such as maximum drawdown,
Calmar ratio or custom risk metrics.
"""

import numpy as np
import pandas as pd


def backtest_strategy(data: pd.DataFrame, predictions: np.ndarray) -> pd.DataFrame:
    """Simulate a simple long/flat trading strategy based on predictions.

    Parameters
    ----------
    data : pandas.DataFrame
        Feature DataFrame containing at least a 'return' column (log returns).
    predictions : numpy.ndarray
        Array of binary predictions aligned with ``data`` indicating when
        to be long (1) or flat (0) on the next bar.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns for strategy returns and cumulative returns.
    """
    df = data.copy()
    # Align predictions to next period: when prediction at t is 1, we take the
    # return of period t+1. Using shift(-1) achieves this.
    df['signal'] = predictions
    df['strategy_return'] = df['return'].shift(-1) * df['signal']
    df.dropna(inplace=True)
    df['cum_return'] = df['strategy_return'].cumsum().apply(np.exp)
    return df


def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0, periods_per_year: int = 252) -> float:
    """Compute the annualised Sharpe ratio of a return series.

    Parameters
    ----------
    returns : pandas.Series
        Strategy returns (log returns).
    risk_free_rate : float, default 0.0
        Risk‑free rate to use in the Sharpe calculation.
    periods_per_year : int, default 252
        Number of return periods per year (252 for daily, 390*252 for minute
        bars etc.).

    Returns
    -------
    float
        Annualised Sharpe ratio.
    """
    # Convert log returns to arithmetic returns for Sharpe calculation
    arith_returns = np.exp(returns) - 1
    excess_returns = arith_returns - (risk_free_rate / periods_per_year)
    if excess_returns.std() == 0:
        return 0.0
    return np.sqrt(periods_per_year) * excess_returns.mean() / excess_returns.std()