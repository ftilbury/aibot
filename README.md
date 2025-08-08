# aibot — Forex‑Focused AI Trading System

This repository houses a fully autonomous AI trading pipeline designed
exclusively for foreign exchange (forex) markets. The system enables a
solo quant to build, test and iterate algorithmic strategies with
institutional‑grade rigour.

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
indicators, experiment with different models or integrate advanced risk
controls. While the current implementation focuses on paper trading and
offline experimentation, it lays the groundwork for live execution
phases.

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

### Running the Pipeline

To train models and backtest strategies on the configured forex pairs
(defined in `config.py`), run:

```bash
python -m main
```

Results will be saved to the `results/` directory as CSV files. The
console will display accuracy, Sharpe ratio and the number of trades for
each symbol.

## 🛠️ Customisation

* **Symbols**: Edit the `SYMBOLS` list in `config.py` to change which
  currency pairs are traded.
* **Indicators**: Add new technical indicators in
  `feature_engineering.py`.
* **Models**: Replace the RandomForest classifier in `model.py` with
  another estimator (e.g. XGBoost or LightGBM) to explore performance
  improvements.
* **Risk Management**: The backtester currently uses a simple
  long/flat strategy with no leverage. Extend `backtest.py` to include
  position sizing, stop‑losses or other controls.
* **Live Trading**: The pipeline is oriented towards research and paper
  trading. A separate execution engine is required to place trades via
  MetaTrader 5; see the `ROADMAP.md` for future development phases.

## 🗺️ Roadmap

The companion file [`ROADMAP.md`](ROADMAP.md) details the phased plan for
expanding this system into a full‑fledged, institution‑worthy trading
platform, including risk engines, dashboards and live trading support.

## 📄 License

This project is licensed under the Apache 2.0 license. See the
[`LICENSE`](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull
requests to improve data handling, add new features or fix bugs.