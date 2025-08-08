"""
Paper execution engine for simulated trading.

The `PaperExecutionEngine` class applies trade signals to market data with
configurable slippage and latency. It opens and closes long positions based
on binary signals (1 for long, 0 for flat) and computes the resulting
account equity curve. Trades are recorded for later analysis or logging.

Example usage:

    engine = PaperExecutionEngine()
    equity_curve = engine.process_signals(df, signals)
    trades = engine.trades

Equity is updated after each bar and stored in ``self.equity_curve``.
"""

from typing import List

import numpy as np
import pandas as pd

from .config import (
    PAPER_TRADE_SLIPPAGE,
    PAPER_TRADE_LATENCY,
    INITIAL_CAPITAL,
)


class Trade:
    """Represents a single trade (long only)."""

    def __init__(self, symbol: str, entry_time, entry_price: float, volume: float) -> None:
        self.symbol = symbol
        self.entry_time = entry_time
        self.entry_price = entry_price
        self.volume = volume
        self.exit_time = None
        self.exit_price = None

    def close(self, exit_time, exit_price: float) -> None:
        self.exit_time = exit_time
        self.exit_price = exit_price

    def pnl(self) -> float:
        if self.exit_price is None:
            return 0.0
        return (self.exit_price - self.entry_price) * self.volume


class PaperExecutionEngine:
    """Simulates trade execution with slippage and latency."""

    def __init__(self, slippage: float = PAPER_TRADE_SLIPPAGE, latency: int = PAPER_TRADE_LATENCY) -> None:
        self.slippage = slippage
        self.latency = latency
        self.trades: List[Trade] = []
        self.capital: float = INITIAL_CAPITAL
        self.equity_curve: List[float] = []

    def _apply_slippage(self, price: float, side: int) -> float:
        """Adjust price for slippage. Side +1 = buy, -1 = sell."""
        return price + side * self.slippage

    def process_signals(self, df: pd.DataFrame, signals: np.ndarray) -> pd.DataFrame:
        """Process trading signals and simulate resulting equity curve.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame with a datetime index and at least a 'close' column.
        signals : numpy.ndarray
            Array of binary signals (length equal to len(df)) indicating
            whether to be long (1) or flat (0) for the next bar.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the equity curve indexed by the timestamps of
            ``df``.
        """
        if len(signals) != len(df):
            raise ValueError("signals length must match data length")
        # Apply latency by shifting signals forward
        delayed_signals = np.roll(signals, self.latency)
        position_open = False
        current_trade = None
        equity = self.capital

        for i in range(len(df) - 1):
            signal = delayed_signals[i]
            next_price = df['close'].iloc[i + 1]
            timestamp = df.index[i + 1]

            if signal == 1 and not position_open:
                # Open a long position
                entry_price = self._apply_slippage(next_price, side=+1)
                current_trade = Trade(symbol=df.name if hasattr(df, 'name') else 'FX',
                                      entry_time=timestamp,
                                      entry_price=entry_price,
                                      volume=1.0)
                position_open = True
            elif signal == 0 and position_open:
                # Close the position
                exit_price = self._apply_slippage(next_price, side=-1)
                current_trade.close(exit_time=timestamp, exit_price=exit_price)
                self.trades.append(current_trade)
                equity += current_trade.pnl()
                position_open = False
            # Append current equity to curve
            self.equity_curve.append(equity)

        # Close any open position at the end of data
        if position_open and current_trade is not None:
            exit_price = self._apply_slippage(df['close'].iloc[-1], side=-1)
            current_trade.close(exit_time=df.index[-1], exit_price=exit_price)
            self.trades.append(current_trade)
            equity += current_trade.pnl()
            self.equity_curve.append(equity)
        
        return pd.DataFrame(self.equity_curve, index=df.index[: len(self.equity_curve)], columns=['equity'])