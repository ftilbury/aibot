"""
Real‑time or paper trading script.

This module orchestrates the process of loading data, generating trade
signals using a trained model, executing trades via the paper execution
engine, enforcing risk limits, logging trades, sending alerts and
optionally running a dashboard.

Run this script as a standalone program once your models have been trained
and saved. For demonstration purposes, it retrains models on the fly; in
production, you should load pre-trained models from disk.
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd

from .config import SYMBOLS, OUTPUT_DIR
from .data_loader import load_data
from .feature_engineering import create_features
from .model import train_model, save_model, load_model
from .execution_engine import PaperExecutionEngine
from .risk_engine import RiskEngine
from .trade_logger import log_trades, log_equity_curve
from .alerts import send_alert


def generate_signals(model, features_df: pd.DataFrame) -> np.ndarray:
    """Generate binary trade signals from a model and feature DataFrame."""
    feature_cols = [col for col in features_df.columns if col not in ['target', 'return', 'strategy_return', 'signal', 'cum_return']]
    X = features_df[feature_cols]
    return model.predict(X)


def trade_symbol(symbol: str, retrain: bool = False) -> None:
    """Trade a single symbol using paper execution.

    Parameters
    ----------
    symbol : str
        Forex pair to trade (e.g. 'EURUSD').
    retrain : bool, default False
        If True, retrain the model from scratch; otherwise load from disk.
    """
    # Load historical data
    df = load_data(symbol)
    df.name = symbol
    # Engineer features and target
    features_df = create_features(df)
    # Model persistence path
    model_path = Path(OUTPUT_DIR) / f"model_{symbol}.joblib"
    if retrain or not model_path.exists():
        # Train model
        X = features_df[[c for c in features_df.columns if c != 'target']]
        y = features_df['target']
        model = train_model(X, y)
        save_model(model, str(model_path))
    else:
        model = load_model(str(model_path))
    # Generate signals (1=long, 0=flat)
    signals = generate_signals(model, features_df)
    # Initialise execution and risk engines
    exec_engine = PaperExecutionEngine()
    risk = RiskEngine()
    # Process signals
    equity_df = exec_engine.process_signals(features_df, signals)
    # Check risk limits
    if not risk.check(exec_engine.capital):
        send_alert(f"Risk limits exceeded on {symbol}; trading halted.")
    # Log trades and equity curve
    trades_file = Path(OUTPUT_DIR) / f"trades_{symbol}.csv"
    equity_file = Path(OUTPUT_DIR) / f"equity_{symbol}.csv"
    log_trades(exec_engine.trades, filepath=str(trades_file))
    log_equity_curve(equity_df, filepath=str(equity_file))
    # Send alerts for each executed trade
    for trade in exec_engine.trades:
        send_alert(
            f"{symbol} trade: enter at {trade.entry_price:.5f} on {trade.entry_time}, exit at {trade.exit_price:.5f} on {trade.exit_time}, PnL: {trade.pnl():.2f}"
        )
    print(f"Completed trading for {symbol}. Final equity: {exec_engine.capital:.2f}")


def main():
    """Trade all symbols configured in config.py."""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    for symbol in SYMBOLS:
        trade_symbol(symbol, retrain=False)


if __name__ == "__main__":
    main()