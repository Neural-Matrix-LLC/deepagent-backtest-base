#!/usr/bin/env python3
"""
Historical Data Fetcher
Fetch and cache price data from various sources.

Usage:
    python fetch_data.py --symbol BTC-USD --period 2y --interval 1d
    python fetch_data.py --symbol ETH-USD --start 2020-01-01 --end 2024-01-01
"""

import argparse
from datetime import datetime, timedelta
from pathlib import Path
import sys


def parse_period(period: str) -> timedelta:
    """Parse period string like '1y', '6m', '30d'."""
    unit = period[-1].lower()
    value = int(period[:-1])
    
    if unit == 'y':
        return timedelta(days=value * 365)
    elif unit == 'm':
        return timedelta(days=value * 30)
    elif unit == 'd':
        return timedelta(days=value)
    elif unit == 'w':
        return timedelta(weeks=value)
    else:
        raise ValueError(f"Unknown period unit: {unit}")


def fetch_yfinance(symbol: str | list[str], start: datetime, end: datetime, interval: str) -> 'pd.DataFrame':
    """Fetch data from Yahoo Finance.
    
    If symbol is a list, downloads all tickers at once with multi-level columns
    and flattens them, e.g. ('Open', 'AAPL') -> 'Open_AAPL'.
    """
    try:
        import yfinance as yf
        import pandas as pd
    except ImportError:
        print("yfinance not installed. Install with: pip install yfinance pandas")
        sys.exit(1)
    
    multi = isinstance(symbol, list)
    label = ', '.join(symbol) if multi else symbol
    print(f"Fetching {label} from Yahoo Finance...")
    
    if multi:
        df = yf.download(symbol, start=start, end=end, interval=interval, multi_level_index=True)
        if df.empty:
            raise ValueError(f"No data returned for {label}")
        # Flatten multi-level columns: ('Open', 'AAPL') -> 'open_AAPL'
        df.columns = [f"{col.lower()}_{ticker}" for col, ticker in df.columns]
    else:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start, end=end, interval=interval)
        if df.empty:
            raise ValueError(f"No data returned for {symbol}")
        df.columns = [c.lower() for c in df.columns]
    
    df.index.name = 'date'
    
    return df


def main():
    parser = argparse.ArgumentParser(description='Fetch historical price data')
    parser.add_argument('--symbol', '-s', required=True, nargs='+', help='Trading symbol(s)')
    parser.add_argument('--period', '-p', help='Lookback period (e.g., 2y, 6m)')
    parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    parser.add_argument('--interval', '-i', default='1d', help='Data interval (1d, 1h, etc.)')
    parser.add_argument('--source', default='yfinance', choices=['yfinance'])
    parser.add_argument('--output', '-o', help='Output directory')
    
    args = parser.parse_args()
    symbols = args.symbol if len(args.symbol) > 1 else args.symbol[0]
    
    # Determine date range
    if args.start and args.end:
        start = datetime.strptime(args.start, '%Y-%m-%d')
        end = datetime.strptime(args.end, '%Y-%m-%d')
    elif args.period:
        end = datetime.now()
        start = end - parse_period(args.period)
    else:
        end = datetime.now()
        start = end - timedelta(days=730)  # 2 years default
    
    # Fetch data
    df = fetch_yfinance(symbols, start, end, args.interval)
    
    # Save to file(s)
    script_dir = Path(__file__).parent
    output_dir = Path(args.output) if args.output else script_dir / 'data'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if isinstance(symbols, list):
        for sym in symbols:
            suffix = f"_{sym}"
            sym_cols = [c for c in df.columns if c.endswith(suffix)]
            sym_df = df[sym_cols].rename(columns={c: c.replace(suffix, '') for c in sym_cols})
            
            filename = f"{sym.replace('/', '_').replace('-', '_')}_{args.interval}.csv"
            output_file = output_dir / filename
            sym_df.to_csv(output_file)
            
            print(f"Data saved to: {output_file}")
            print(f"  Rows: {len(sym_df)}")
            print(f"  Date range: {df.index[0]} to {df.index[-1]}")
            print(f"  Columns: {list(sym_df.columns)}")
    else:
        filename = f"{symbols.replace('/', '_').replace('-', '_')}_{args.interval}.csv"
        output_file = output_dir / filename
        df.to_csv(output_file)
        
        print(f"Data saved to: {output_file}")
        print(f"  Rows: {len(df)}")
        print(f"  Date range: {df.index[0]} to {df.index[-1]}")
        print(f"  Columns: {list(df.columns)}")


if __name__ == '__main__':
    main()