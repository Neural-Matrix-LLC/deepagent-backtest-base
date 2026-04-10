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
python fetch_data.py -s AAPL -p 2y
```

**Multiple tickers (space-separated, NOT comma-separated):**
```bash
python fetch_data.py -s PIN FXI EWI EWW EZA EWT EWJ IVV EWU EZU EWA EWS EWC EIS EWZ -p 2y
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

If `fetch_data.py` raises any exception, capture the full error message **and** traceback into `backtest_error.txt`.
Use a command like:
```bash
python fetch_data.py -s AAPL -p 2y 2>&1 || python -c "
import traceback, sys
with open('backtest_error.txt','w') as f:
    f.write(open('/dev/stdin').read())
" 
```
Or, more reliably, wrap the call so stderr+stdout are captured:
```bash
python fetch_data.py -s AAPL -p 2y > /tmp/fetch_output.txt 2>&1
if [ $? -ne 0 ]; then
  cp /tmp/fetch_output.txt backtest_error.txt
fi
```
If `backtest_error.txt` is produced at this stage, **STOP immediately** — do NOT proceed to run `backtest.py`. Your task is done.

### Verify

After fetching (only if no error), confirm files exist:
```bash
ls data/
```

## Step 3: Run the backtest

Run `backtest.py` from the project root directory. (All parameters read from `settings.yaml`)

**Single-asset strategy or multi-asset strategy:**
```bash
python backtest.py --strategy custom_trading_strategy
```

### CLI options

| Flag | Description | Default |
|---|---|---|
| `--strategy` / `-s` | Strategy name from `STRATEGIES` dict (required) | — |

### Error handling for backtest.py

If `backtest.py` raises any exception, capture the full error message **and** traceback into `backtest_error.txt`.
Wrap the call so stderr+stdout are captured:
```bash
python backtest.py --strategy custom_trading_strategy --symbol AAPL --period 2y > /tmp/backtest_output.txt 2>&1
if [ $? -ne 0 ]; then
  cp /tmp/backtest_output.txt backtest_error.txt
fi
```
If `backtest_error.txt` is produced, **STOP immediately**. Your task is done — the debugging agent will handle the fix.

### Routing

The engine auto-routes based on the strategy's `multi_asset` attribute:
- `multi_asset = False` → `run_backtest()` — bar-by-bar simulation with stop-loss/take-profit.
- `multi_asset = True` → `run_multi_backtest()` — vectorized portfolio simulation, equal-weighted positions.


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

Read the summary to verify the backtest completed successfully:
```bash
cat reports/*_summary.txt | tail -1
```

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `Unknown strategy: X` | Strategy not registered | Code agent must add it to `STRATEGIES` dict |
| `No data returned for X` | Invalid ticker or no market data | Check ticker symbol spelling |
| `Insufficient data. Got N bars` | Too few bars for strategy lookback | Use a longer `--period` |
| `--symbol is required` | Single-asset strategy needs a ticker | Pass `--symbol TICK` |
| `AttributeError: 'Index' ... 'tz'` | Stale cached CSV | Delete the CSV in `data/` and re-fetch |

