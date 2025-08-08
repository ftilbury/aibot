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

# Initial account capital (in account currency). This value is used by the
# risk engine to compute drawdowns and daily loss thresholds.
INITIAL_CAPITAL = 100_000.0

# Simulated slippage to apply on each executed trade. Expressed as the price
# difference (e.g. 0.00001 for 0.1 pip on most forex pairs). Larger values
# emulate worse fills.
PAPER_TRADE_SLIPPAGE = 0.00001

# Simulated latency before orders are executed, measured in number of bars. A
# value of 1 means signals are delayed by one bar before being acted upon.
PAPER_TRADE_LATENCY = 1

# Maximum trailing drawdown allowed (as a fraction of initial capital). If
# the equity falls more than this amount below its peak, trading stops.
MAX_DRAWDOWN = 0.10

###############################################################################
# Output and persistence
###############################################################################

# Directory where models and backtest results will be saved.
OUTPUT_DIR = "results"

###############################################################################
# Telegram alert configuration
###############################################################################

# Telegram bot token and chat ID for sending alert notifications. Replace
# these values with your own. Keep these credentials secret and avoid
# publishing them publicly.
TELEGRAM_BOT_TOKEN = "7776300177:AAEr79a9Wpg90dUUNcJhpQve4k-0tA2q8eI"
TELEGRAM_CHAT_ID = "5542080541"
