# aibot — Forex‑Focused AI Trading System

This repository houses a fully autonomous AI trading platform designed
exclusively for foreign exchange (forex) markets. The system enables a
solo quant to build, test, iterate and execute algorithmic strategies
with institutional‑grade rigour. Beyond backtesting, the platform
includes a paper execution engine, risk management, trade logging,
Telegram alerts and a configurable dashboard.

## 📈 Overview

The project provides an end‑to‑end workflow:

1. **Data Ingestion**: Pull historical forex price data directly from MetaTrader 5.
2. **Feature Engineering**: Compute technical indicators such as moving averages,
   RSI and Bollinger bandwidth.
3. **Machine Learning**: Train a classifier (RandomForest by default) to
   predict the direction of the next bar.
4. **Backtesting**: Simulate trades on unseen data and compute metrics such
   as cumulative return and Sharpe ratio.
5. **Evaluation**: Summarise classification and strategy performance and
   persist results for later analysis.

The design is modular so you can swap out data sources, add new
indicators, experiment with different models (including deep learning
architectures) and integrate advanced risk controls. The platform
supports paper trading with realistic slippage and latency, risk
management (daily loss and trailing drawdown limits), Telegram alerts
and a browser‑based dashboard. It lays the groundwork for live
execution phases and future enhancements.

## ⚙️ Getting Started

### Prerequisites

* Python 3.10+
* [MetaTrader 5](https://www.metatrader5.com/) installed and logged in to
  a broker account (demo or live)

### Installation

Clone this repository and install dependencies:

```bash
git clone https://github.com/ftilbury/aibot.git
cd aibot
pip install -r requirements.txt
```

Ensure the MetaTrader 5 terminal is running on the same machine before
executing the pipeline.

### Running the Research Pipeline

To train models and backtest strategies on the configured forex pairs
(defined in `config.py`), run:

```bash
python -m main
```

Results will be saved to the `results/` directory as CSV files. The
console will display accuracy, Sharpe ratio and the number of trades for
each symbol.

### Running the Paper Trading Engine

Once models have been trained and saved in the `results/` directory, you
can simulate live trading using the paper execution engine:

```bash
python -m trade
```

This script loads the latest data, generates signals with the saved
models, executes trades via the paper engine, enforces risk limits, logs
trades, sends Telegram notifications and stores the equity curve. You
can customise execution and risk parameters in `config.py`.

## 🛠️ Customisation

* **Symbols**: Edit the `SYMBOLS` list in `config.py` to change which
  currency pairs are traded.
* **Indicators**: Add new technical indicators in
  `feature_engineering.py`.
* **Models**: Replace the RandomForest classifier in `model.py` with
  another estimator (e.g. XGBoost or LightGBM) to explore performance
  improvements.
* **Risk Management**: Use the risk engine (`risk_engine.py`) to
  enforce daily loss and trailing drawdown limits. Extend it to include
  position sizing, stop‑losses or other controls.
* **Live Trading**: The pipeline is oriented towards research and paper
  trading. A separate execution engine is required to place trades via
  MetaTrader 5; see the `ROADMAP.md` for future development phases.

## 🗺️ Roadmap

The companion file [`ROADMAP.md`](ROADMAP.md) details the phased plan for
expanding this system into a full‑fledged, institution‑worthy trading
platform. With the introduction of the execution engine, risk
management and alerting, the project has moved into Phase 2. This sets
the stage for future milestones such as portfolio optimisation, cloud
deployment, auto‑retraining of models and live trading support.

## 📄 License

This project is licensed under the Apache 2.0 license. See the
[`LICENSE`](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull
requests to improve data handling, add new features or fix bugs.