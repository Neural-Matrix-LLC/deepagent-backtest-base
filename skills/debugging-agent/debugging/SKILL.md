---
name: debugging
description: Read errors from backtest_error.txt, diagnose the root cause, and fix the strategy code. Does not execute code.
---

# Debugging Skill — Backtest Error Fix

## Available Tools

`read_file`, `write_file`, `edit_file`, `ls`, `grep`, `glob`, `write_todos`, `delete_file`, `ruff_format`

## Folder Structure
All files are at the ROOT of the working directory. There are no subdirectories.
Never prefix filenames with a directory name or forward slash.

Key files:
- backtest_error.txt (read this for errors — may contain failures from fetch_data.py or backtest.py)
- customtradingstrategy/customtradingstrategy.py (strategy implementations — this is the PRIMARY file to fix)
- config/settings.yaml (default parameters for strategies — may also need fixes)
- strategy.json (reference — the original strategy rules)
- backtest.py, fetch_data.py, metrics.py, strategies.py (execution scripts — do NOT modify these)

## Workflow
1. Read backtest_error.txt to understand the error messages and call stack.
2. Determine the error source:
   - Errors from **fetch_data.py** (e.g., bad ticker symbols, invalid parameters) → check the parameters passed into the script.
   - Errors from **backtest.py** (e.g., strategy logic bugs, signal issues) → fix `customtradingstrategy/customtradingstrategy.py` and/or `config/settings.yaml`.
3. Read the relevant file(s) to inspect the code.
4. Identify the root cause of the error.
5. Apply the fix using edit_file (preferred) or write_file (full rewrite only if necessary).
6. Call the `ruff_format` tool on every Python file you edited to auto-format the fixed code and catch any linting issues.
   If the tool returns any errors, fix them and re-run `ruff_format` until there are no issues.
7. Delete backtest_error.txt using delete_file.
8. STOP. Your turn is DONE.

## Constraints
- Do NOT modify `backtest.py`, `fetch_data.py`, `strategies.py` or `metrics.py`. Only fix `customtradingstrategy/customtradingstrategy.py` and/or `config/settings.yaml`.
- After editing the file(s) and deleting the error file, STOP immediately.
- Do NOT call the execute tool. Do NOT run python, bash, or any shell command.
- Do NOT attempt to test, validate, or run the fixed code.
- Do NOT check if the fix works — the backtest-agent handles execution next.
