"""
Risk management engine for trading strategies.

This module defines a simple risk management engine that enforces daily
loss limits and trailing drawdown limits. It tracks the account equity
throughout the trading day and determines whether trading should be halted.

Example usage:

    risk = RiskEngine()
    if not risk.check(current_equity):
        # Stop trading and raise an alert

"""

from datetime import date

from .config import MAX_DAILY_LOSS, MAX_DRAWDOWN, INITIAL_CAPITAL


class RiskEngine:
    """Monitors account equity against risk limits."""

    def __init__(self) -> None:
        self.daily_start = date.today()
        self.start_equity = INITIAL_CAPITAL
        self.peak_equity = INITIAL_CAPITAL

    def reset_daily(self, equity: float) -> None:
        """Reset the daily tracking variables (call at start of a new day)."""
        self.daily_start = date.today()
        self.start_equity = equity
        self.peak_equity = equity

    def check(self, equity: float) -> bool:
        """Check if trading is allowed given the current equity.

        Returns
        -------
        bool
            True if trading may continue, False if risk limits are exceeded.
        """
        # Reset daily metrics if a new day has started
        if date.today() != self.daily_start:
            self.reset_daily(equity)

        # Daily drawdown relative to initial capital
        daily_drawdown = (self.start_equity - equity) / INITIAL_CAPITAL
        if daily_drawdown > MAX_DAILY_LOSS:
            return False

        # Update peak equity and compute trailing drawdown
        if equity > self.peak_equity:
            self.peak_equity = equity
        trailing_drawdown = (self.peak_equity - equity) / INITIAL_CAPITAL
        if trailing_drawdown > MAX_DRAWDOWN:
            return False

        return True