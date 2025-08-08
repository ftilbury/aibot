"""
Trade logging utilities.

This module defines functions to persist executed trades and equity
curves to CSV files for later analysis. Logging can be extended to
databases or other storage backends as required.
"""

import pandas as pd
from typing import List

from .execution_engine import Trade


def log_trades(trades: List[Trade], filepath: str = "trades.csv") -> None:
    """Save a list of trades to a CSV file.

    Parameters
    ----------
    trades : list of Trade
        List of completed trades.
    filepath : str, default "trades.csv"
        Path to the output CSV file.
    """
    records = []
    for trade in trades:
        records.append({
            'symbol': trade.symbol,
            'entry_time': trade.entry_time,
            'entry_price': trade.entry_price,
            'exit_time': trade.exit_time,
            'exit_price': trade.exit_price,
            'pnl': trade.pnl(),
        })
    if not records:
        return
    df = pd.DataFrame(records)
    df.to_csv(filepath, index=False)


def log_equity_curve(equity_df: pd.DataFrame, filepath: str = "equity_curve.csv") -> None:
    """Save the equity curve DataFrame to a CSV file."""
    equity_df.to_csv(filepath, index=True)