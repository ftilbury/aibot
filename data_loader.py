"""
Data loading utilities for forex trading.

This module provides functions to retrieve historical price data for forex
currency pairs using MetaTrader 5. It abstracts away the details of
initialising and connecting to the MT5 platform and returns data in a
clean pandas DataFrame ready for feature engineering.

If MetaTrader5 is not installed or you prefer another data source, you
can replace the `load_data` function with calls to your chosen API or
data provider. Ensure that the resulting DataFrame has at least the
columns: time, open, high, low, close, tick_volume, spread, real_volume.

"""

from datetime import datetime
from typing import List, Optional

import pandas as pd
import MetaTrader5 as mt5

from .config import TIMEFRAME, START_DATE, END_DATE


def _initialize_mt5() -> None:
    """Initialise the MetaTrader 5 terminal.

    Raises:
        RuntimeError: if the terminal could not be initialised.
    """
    if not mt5.initialize():
        raise RuntimeError(
            f"MetaTrader5 initialise failed, error code: {mt5.last_error()}"
        )


def load_data(
    symbol: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    timeframe: Optional[int] = None,
) -> pd.DataFrame:
    """Load historical OHLCV data for a given forex symbol.

    Parameters
    ----------
    symbol : str
        The forex symbol to load (e.g. "EURUSD").
    start_date : datetime, optional
        The start date for the historical data. Defaults to START_DATE.
    end_date : datetime, optional
        The end date for the historical data. Defaults to END_DATE.
    timeframe : int, optional
        MT5 timeframe constant. Defaults to TIMEFRAME.

    Returns
    -------
    pandas.DataFrame
        A DataFrame indexed by time with columns: open, high, low, close,
        tick_volume, spread, real_volume.

    Raises
    ------
    RuntimeError
        If data could not be retrieved from MT5.
    """
    start = start_date or START_DATE
    end = end_date or END_DATE
    tf = timeframe or TIMEFRAME

    # Ensure MT5 terminal is running
    _initialize_mt5()

    # Request price history
    rates = mt5.copy_rates_range(symbol, tf, start, end)
    if rates is None or len(rates) == 0:
        raise RuntimeError(f"No data returned for {symbol}. Please check the symbol and date range.")

    df = pd.DataFrame(rates)
    # Convert timestamp to datetime
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df.set_index('time')
    return df


def load_all_symbols(symbols: List[str]) -> dict:
    """Load data for all symbols in a list.

    Parameters
    ----------
    symbols : list of str
        Currency pairs to load.

    Returns
    -------
    dict
        A mapping of symbol → DataFrame.
    """
    data = {}
    for symbol in symbols:
        try:
            data[symbol] = load_data(symbol)
        except RuntimeError as e:
            print(f"Warning: could not load {symbol}: {e}")
    return data