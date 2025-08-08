"""
LSTM model utilities.

This module provides an example implementation of a Long Short‑Term Memory
(LSTM) neural network using Keras/TensorFlow. It demonstrates how to build
and train an LSTM on sequences of features for predicting price direction.

Note: Training deep learning models for trading requires careful tuning,
proper handling of non-stationary data and consideration of lookahead
bias. This example is provided for educational purposes.
"""

import numpy as np
import pandas as pd
from typing import Tuple

try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense
except ImportError:
    Sequential = None  # type: ignore


def _to_sequences(X: np.ndarray, y: np.ndarray, seq_len: int) -> Tuple[np.ndarray, np.ndarray]:
    """Convert flat arrays into sequences for LSTM input."""
    Xs, ys = [], []
    for i in range(len(X) - seq_len):
        Xs.append(X[i : i + seq_len])
        ys.append(y[i + seq_len])
    return np.array(Xs), np.array(ys)


def build_lstm_model(input_shape: Tuple[int, int]):
    """Build a simple LSTM model."""
    if Sequential is None:
        raise ImportError("TensorFlow is not installed. Cannot build LSTM model.")
    model = Sequential()
    model.add(LSTM(50, input_shape=input_shape))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


def train_lstm(X: pd.DataFrame, y: pd.Series, seq_len: int = 20, epochs: int = 10, batch_size: int = 32):
    """Train an LSTM model on sequential data.

    Parameters
    ----------
    X : pandas.DataFrame
        Feature matrix.
    y : pandas.Series
        Binary labels.
    seq_len : int, default 20
        Length of sequences to feed into the LSTM.
    epochs : int, default 10
        Number of training epochs.
    batch_size : int, default 32
        Batch size for training.
    """
    if Sequential is None:
        raise ImportError("TensorFlow is not installed. Cannot train LSTM model.")
    # Convert to numpy arrays
    X_np = X.to_numpy()
    y_np = y.to_numpy()
    # Build sequences
    X_seq, y_seq = _to_sequences(X_np, y_np, seq_len)
    # Build model
    model = build_lstm_model(input_shape=(seq_len, X_seq.shape[2] if len(X_seq.shape) > 2 else X_seq.shape[1]))
    # Reshape if necessary
    if len(X_seq.shape) == 2:
        # If only one feature, reshape to (samples, seq_len, 1)
        X_seq = X_seq.reshape((X_seq.shape[0], X_seq.shape[1], 1))
    # Train model
    model.fit(X_seq, y_seq, epochs=epochs, batch_size=batch_size, verbose=0)
    return model