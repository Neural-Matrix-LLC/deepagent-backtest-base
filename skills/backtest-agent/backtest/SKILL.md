---
name: backtest
description: Fetch historical data and run a backtest for a strategy that has already been implemented. This agent executes CLI commands only — it does NOT modify code files.
---

## Available Tools

`execute`, `ls`, `glob`, `write_todos`, `read_file`, `grep`

Do NOT edit `strategies.py`, `backtest.py`, `fetch_data.py`, `metrics.py`, `customstrategy/customtradingstrategy.py` or `config/settings.yaml`.
Knowing the presence of these files using ls is sufficient. You do NOT need to read their contents.

## Prerequisites

### Python environment setup

Before running any scripts, ensure a virtual environment exists and dependencies are installed:
```bash
python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt
```
If `.venv/` already exists, just activate it:
```bash
.venv/bin/activate

If there is backtest_error.txt from a previous run, delete it before proceeding:
```bash
rm -f backtest_error.txt
```

### Code readiness

The code-writing agent has already:
1. Edited the `CustomTradingStrategy` class in `customstrategy/customtradingstrategy.py`.
2. Added default parameters to `config/settings.yaml` under the `custom_trading_strategy:` key.

## Step 1: Read the strategy config

Read `config/settings.yaml` to determine:
- The **strategy name** (always `custom_trading_strategy`).
- The **ticker list** (either a `tickers:` list for multi-asset, or a single symbol provided by the user).
- Any **default parameters** to verify.

Also read `customstrategy/customtradingstrategy.py` and check the `multi_asset` attribute on the strategy class to determine whether this is single-asset or multi-asset.

## Step 2: Fetch historical data

Run `fetch_data.py` from the project root directory.

**Single ticker:**
```bash
.venv/bin/python fetch_data.py -s AAPL -p 2y
```

**Multiple tickers (space-separated, NOT comma-separated):**
```bash
.venv/bin/python fetch_data.py -s PIN FXI EWI EWW EZA EWT EWJ IVV EWU EZU EWA EWS EWC EIS EWZ -p 2y
```

### CLI options

| Flag | Description | Default |
|---|---|---|
| `-s` / `--symbol` | One or more tickers (required, space-separated) | — |
| `-p` / `--period` | Lookback: `2y`, `6m`, `30d` | 2y |
| `--start` / `--end` | Explicit date range (YYYY-MM-DD) | — |
| `-i` / `--interval` | Bar size | `1d` |
| `-o` / `--output` | Output directory | `./data` |

Data is cached as `{TICKER}_{interval}.csv` in the data directory. For multiple tickers, one CSV per ticker.

### Error handling for fetch_data.py

If `fetch_data.py` raises any exception, error message **and** traceback will be written into `backtest_error.txt`.
Use a command like:
```bash
.venv/bin/python fetch_data.py -s AAPL -p 2y
```

If `backtest_error.txt` is produced at this stage, **STOP immediately** — do NOT proceed to run `backtest.py`. 

### Verify

After fetching (only if no error), confirm files exist:
```bash
ls data/
```

## Step 3: Run the backtest

Run `backtest.py` from the project root directory. (All parameters read from `settings.yaml`)

**Single-asset strategy or multi-asset strategy:**
```bash
.venv/bin/python backtest.py --strategy custom_trading_strategy
```

### Error handling for backtest.py

If `backtest.py` raises any exception, error message **and** traceback will be written into `backtest_error.txt`.

If `backtest_error.txt` is produced, **STOP immediately**. 
Your task is done — DO NOT try to look into the code to fix it yourself; the debugging agent will handle the fix.


## Step 4: Verify output

Results are saved to `./reports/` (or the `--output` dir):

| File | Contents |
|---|---|
| `*_summary.txt` | Formatted performance report (return, Sharpe, drawdown, etc.) |
| `*_trades.csv` | Trade log with entry/exit times, prices, PnL |
| `*_equity.csv` | Daily equity curve |
| `*_chart.png` | Equity + drawdown chart (requires matplotlib) |

Confirm results:
```bash
ls reports/
```
## Step 5: Remove virtual environment

After verifying the backtest results, clean up by removing the virtual environment:
```bash
rm -rf .venv
```


