"""
Machine learning model utilities.

This module defines functions for training and using machine‑learning models
to predict future price direction based on engineered features. It uses
scikit‑learn under the hood and currently defaults to a RandomForest
classifier. You can experiment with other classifiers (e.g. XGBoost,
LightGBM) by substituting the estimator class.
"""

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from .config import RANDOM_STATE, OUTPUT_DIR


def train_model(X: pd.DataFrame, y: pd.Series) -> RandomForestClassifier:
    """Train a RandomForest classifier on the provided features and labels.

    Parameters
    ----------
    X : pandas.DataFrame
        Feature matrix.
    y : pandas.Series
        Binary target labels.

    Returns
    -------
    RandomForestClassifier
        The trained model.
    """
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    model.fit(X, y)
    return model


def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> float:
    """Evaluate the trained model on a hold‑out set.

    Returns accuracy as a simple diagnostic. For trading, more nuanced
    metrics (e.g. precision, recall) may be considered depending on
    class imbalance and risk appetite.
    """
    preds = model.predict(X_test)
    return accuracy_score(y_test, preds)


def save_model(model: RandomForestClassifier, path: str) -> None:
    """Persist the model to disk using joblib."""
    joblib.dump(model, path)


def load_model(path: str) -> RandomForestClassifier:
    """Load a persisted model from disk."""
    return joblib.load(path)