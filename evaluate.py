"""
Evaluation utilities for trading strategies.

This module provides functions to summarise the performance of trained
models and backtested strategies. It can produce metrics such as
accuracy, precision and Sharpe ratio. Additional metrics can be added
as needed.
"""

from typing import Dict, Any

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score

from .backtest import sharpe_ratio


def evaluate_classification(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Compute classification performance metrics.

    Parameters
    ----------
    y_true : numpy.ndarray
        True binary labels.
    y_pred : numpy.ndarray
        Predicted binary labels.

    Returns
    -------
    dict
        Dictionary containing accuracy, precision and recall.
    """
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
    }


def evaluate_strategy(returns: pd.Series) -> Dict[str, Any]:
    """Compute performance metrics for strategy returns.

    Parameters
    ----------
    returns : pandas.Series
        Log returns of the trading strategy.

    Returns
    -------
    dict
        Dictionary containing cumulative return and Sharpe ratio.
    """
    cumulative_return = float(np.exp(returns.sum()) - 1)
    sharpe = sharpe_ratio(returns)
    return {
        "cumulative_return": cumulative_return,
        "sharpe_ratio": sharpe,
    }