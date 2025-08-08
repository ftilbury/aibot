"""
Entrypoint for the forex AI trading pipeline.

This script orchestrates the end‑to‑end workflow:

1. Load historical data for each forex pair.
2. Engineer features.
3. Train a machine‑learning model.
4. Evaluate the model on a hold‑out set.
5. Backtest the trading strategy based on model predictions.
6. Report performance metrics.

The goal is to demonstrate a simple yet extensible pipeline that can be
expanded with additional features, models and risk controls. It is
designed for offline experimentation and paper trading. Live execution
should be handled via a dedicated execution engine (Phase 2).
"""

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from .config import SYMBOLS, OUTPUT_DIR, RANDOM_STATE
from .data_loader import load_all_symbols
from .feature_engineering import create_features
from .model import train_model, evaluate_model
from .backtest import backtest_strategy
from .evaluate import evaluate_classification, evaluate_strategy


def train_and_backtest() -> Dict[str, Dict[str, float]]:
    """Train models and backtest strategies for all configured symbols.

    Returns
    -------
    dict
        Nested dictionary keyed by symbol containing evaluation metrics.
    """
    results = {}

    # Ensure output directory exists
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Load data for all forex symbols
    symbol_data = load_all_symbols(SYMBOLS)

    for symbol, df in symbol_data.items():
        print(f"Processing {symbol}...")
        # Engineer features and target
        features_df = create_features(df)
        X = features_df[[col for col in features_df.columns if col not in ['target', 'return', 'strategy_return', 'signal', 'cum_return']]]
        y = features_df['target']

        # Train/test split (80/20, time‑ordered)
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

        # Train model
        model = train_model(X_train, y_train)
        # Evaluate classifier
        y_pred_test = model.predict(X_test)
        clf_metrics = evaluate_classification(y_test.values, y_pred_test)
        accuracy = clf_metrics['accuracy']

        # Backtest strategy on test period
        backtest_df = backtest_strategy(features_df.iloc[split_idx:].copy(), y_pred_test)
        strat_metrics = evaluate_strategy(backtest_df['strategy_return'])

        results[symbol] = {
            **clf_metrics,
            **strat_metrics,
            'num_trades': int(backtest_df['signal'].sum()),
        }

        # Save results to CSV for further analysis
        backtest_path = Path(OUTPUT_DIR) / f"backtest_{symbol}.csv"
        backtest_df.to_csv(backtest_path)

        print(f"{symbol} — Accuracy: {accuracy:.4f}, Sharpe: {strat_metrics['sharpe_ratio']:.2f}, Trades: {results[symbol]['num_trades']}")

    return results


if __name__ == "__main__":
    train_and_backtest()