"""
Configuration settings for the forex-focused AI trading system.

This module centralises parameters controlling which forex pairs are traded,
the date range for backtesting, and default model hyperparameters. By
consolidating these values, you can easily tweak the behaviour of the
pipeline without hunting through multiple files.

The system is deliberately scoped to foreign exchange (forex) trading.
Only currency pairs defined in the `SYMBOLS` list will be considered. If
you wish to experiment with additional pairs, add them to this list.

Example usage:

    from config import SYMBOLS, START_DATE, END_DATE
    for symbol in SYMBOLS:
        df = load_data(symbol)

"""

from datetime import datetime

import MetaTrader5 as mt5

###############################################################################
# Market and broker settings
###############################################################################

# Symbols to trade. Limit this list strictly to forex pairs to avoid
# inadvertently trading other asset classes. These are some of the most
# liquid currency pairs. Feel free to adjust the list to suit your
# preferences or broker availability.
SYMBOLS = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "USDCHF",
    "USDCAD",
    "AUDUSD",
    "NZDUSD",
]

# MetaTrader 5 timeframe constant. Default to M15 (15‑minute bars). You can
# choose other timeframes supported by MT5 (e.g. TIMEFRAME_M1, TIMEFRAME_H1).
TIMEFRAME = mt5.TIMEFRAME_M15

# Historical window for backtesting. Adjust the start date to control how
# much data is used to train and evaluate models. `END_DATE` defaults to now.
START_DATE = datetime(2019, 1, 1)
END_DATE = datetime.now()

###############################################################################
# Model and training parameters
###############################################################################

# Number of past bars used as features in sequence models (if used). For
# classical models we use technical indicators instead, so this parameter is
# included here for completeness and future expansion.
LOOKBACK_WINDOW = 60

# Random seed for reproducible results.
RANDOM_STATE = 42

###############################################################################
# Risk management
###############################################################################

# Maximum allowable percentage drawdown in a single day. Used by the risk
# engine to halt trading if exceeded (for live trading).
MAX_DAILY_LOSS = 0.025  # 2.5%

###############################################################################
# Output and persistence
###############################################################################

# Directory where models and backtest results will be saved.
OUTPUT_DIR = "results"
