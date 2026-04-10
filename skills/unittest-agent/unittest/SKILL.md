---
name: unittest
description: Write a self-contained Python unit test script for the customtradingstrategy.py file. Produces test_customtradingstrategy.py with unit tests for the Strategy class, then runs the tests and writes results to unittest_report.txt.
---
# Unit Test Skill — Custom Trading Strategy Unit Testing

## Input
Read customstrategy/customtradingstrategy.py from the working directory — it contains the Strategy class.

## Output
If the file test_customtradingstrategy.py does not already exist in the workspace:
Write a single Python script to test_customtradingstrategy.py using write_file tool.
The script should use the unittest framework to define test cases for the Strategy class and its methods.

If the file test_customtradingstrategy.py already exists:
That means this agent has already been run once, and the test script is in place. In this case, skip writing the file and proceed to running the tests.

In either case, executing the tests will produce a file named `unittest_report.txt`, which contains the results of running the unit tests.

## Prerequisites

### Python environment setup

Before running any scripts, ensure a virtual environment exists and dependencies are installed:
```bash
python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt
```
If `.venv/` already exists, just activate it (Take note the correct path is just .venv/, not /.venv/ as the folder is at the root of the working directory):
```bash
.venv/bin/activate
```

## Procedure

Follow these steps in order:

**STEP 1 — Write the test file**
Read customstrategy/customtradingstrategy.py, then write test_customtradingstrategy.py following the Code Structure below.

**STEP 2 — Format the test file**
Call the `ruff_format` tool with `file_path` set to `"test_customtradingstrategy.py"`.
If it reports any errors, fix them and re-run `ruff_format` until the file is clean.

**STEP 3 — Set up the environment and run the tests**
Execute the following bash command in sequence:

```bash
.venv/bin/python3.12 test_customtradingstrategy.py
```

**STEP 4 — Stop**
Do **not** attempt to fix or modify the test script based on test results. Whether the tests pass or fail, your job is done once the tests have been executed and the report written.
Respond with only: "Done." The orchestrator reads unittest_report.txt to determine pass/fail.

## Code Structure
The script must have 3 parts:

### Part 1: Imports
All necessary imports (unittest, the Strategy class from customstrategy.customtradingstrategy, and any dependencies).

### Part 2: Test Class
A single test class inheriting from `unittest.TestCase` with one `setUp` method and multiple `test_*` methods.

### Part 3: Entry Point
Do **not** use `unittest.main()`. Instead, use a `TextTestRunner` that writes its output to `unittest_report.txt`:

```python
if __name__ == "__main__":
    with open("unittest_report.txt", "w") as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestStrategy)  # replace with actual class name
        runner.run(suite)
```

---

## Python unittest Basics

### Defining a Test Class and Methods
```python
import unittest

class TestMyThing(unittest.TestCase):

    def setUp(self):
        # Runs before every test method — set up shared fixtures here
        self.value = 42

    def tearDown(self):
        # Runs after every test method — clean up resources here
        pass

    def test_something(self):
        # Every test method name must start with test_
        self.assertEqual(self.value, 42)
```

### Common Assertion Methods
| Assertion | Checks |
|---|---|
| `assertEqual(a, b)` | `a == b` |
| `assertNotEqual(a, b)` | `a != b` |
| `assertTrue(x)` | `bool(x) is True` |
| `assertFalse(x)` | `bool(x) is False` |
| `assertIsNone(x)` | `x is None` |
| `assertIsNotNone(x)` | `x is not None` |
| `assertIn(a, b)` | `a in b` |
| `assertAlmostEqual(a, b, places=5)` | floats approx equal |
| `assertRaises(ExcType, fn, *args)` | fn(*args) raises ExcType |
| `assertGreater(a, b)` | `a > b` |
| `assertGreaterEqual(a, b)` | `a >= b` |

### Testing for Exceptions
```python
def test_raises_on_empty_data(self):
    with self.assertRaises(ValueError):
        process([])   # must raise ValueError

# Or use the callable form:
self.assertRaises(KeyError, my_dict.__getitem__, "missing_key")
```

### Mocking External Dependencies
Use `unittest.mock` to isolate units from file I/O, network calls, or heavy computation.

```python
from unittest.mock import patch, MagicMock

class TestStrategy(unittest.TestCase):

    @patch("backtest.yf.download")          # patch at the point of USE
    def test_download_called_with_ticker(self, mock_download):
        mock_download.return_value = pd.DataFrame(...)   # fake data
        result = download_data("BTC-USD", "2023-01-01", "2023-12-31")
        mock_download.assert_called_once()
        self.assertIsNotNone(result)

    def test_with_mock_object(self):
        mock_df = MagicMock()
        mock_df.__len__.return_value = 100
        self.assertEqual(len(mock_df), 100)
```

### Parametrizing Tests (subTest)
Run the same assertion across multiple inputs without writing separate methods.

```python
def test_signal_values(self):
    cases = [
        (100.0, 95.0, 1),    # price above MA → buy
        (90.0, 95.0, -1),   # price below MA → sell
        (95.0, 95.0, 0),    # price equals MA → flat
    ]
    for price, ma, expected in cases:
        with self.subTest(price=price, ma=ma):
            self.assertEqual(compute_signal(price, ma), expected)
```

### Skipping Tests
```python
@unittest.skip("not implemented yet")
def test_future_feature(self):
    ...

@unittest.skipIf(condition, "reason")
def test_platform_specific(self):
    ...
```

### Testing Pandas / Numeric Results
Always use `assertAlmostEqual` or pandas/numpy helpers for floats.

```python
import pandas as pd
import numpy as np

def test_pnl_column_exists(self):
    self.assertIn("pnl", self.result.columns)

def test_sharpe_positive(self):
    self.assertGreater(self.result["sharpe"].iloc[-1], 0)

def test_returns_close_to_expected(self):
    self.assertAlmostEqual(self.result["total_return"], 0.15, places=2)

def test_no_nan_in_signals(self):
    self.assertFalse(self.signals.isna().any())
```

### Running Tests from the Terminal
```bash
# Run the script directly — this produces unittest_report.txt
python test_backtest.py

# Inspect the report
cat unittest_report.txt
```

Avoid `python -m unittest` for this project — it does not write to `unittest_report.txt`.

### Generating the Report Programmatically
`unittest.TextTestRunner` accepts a `stream` argument. Passing an open file handle redirects all output (dots, test names, errors, the summary line) to that file.

```python
import unittest

if __name__ == "__main__":
    with open("unittest_report.txt", "w") as report:
        runner = unittest.TextTestRunner(stream=report, verbosity=2)
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestStrategy)
        result = runner.run(suite)
    # Exit with non-zero code if any test failed (useful in CI)
    raise SystemExit(0 if result.wasSuccessful() else 1)
```

`verbosity=2` writes one line per test (`test_signal_generation ... ok`). Use `verbosity=1` for the compact dot format.

---

## Conventions for this Project

- Test file name: `test_backtest.py` in the project root.
- Import the subject under test at the top — use `sys.path` insertion if needed:
  ```python
  import sys, os
  sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
  from backtest import Strategy
  ```
- Use `setUp` to instantiate a `Strategy` with minimal/mock data so every test starts from a clean state.
- Keep each `test_*` method focused on **one behaviour** — short and readable.
- Prefer `assertAlmostEqual` / `assertGreater` for all float/metric comparisons.
- Mock `yf.download` (or any network call) so tests run offline and deterministically.
- The entry point **must** use `TextTestRunner(stream=f, verbosity=2)` writing to `unittest_report.txt`. Do not call `unittest.main()`.

