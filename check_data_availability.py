#!/usr/bin/env python3
"""Check historical data availability for all tickers"""

import yfinance as yf
from datetime import datetime

# All tickers from SECTORS
TICKERS = [
    "XLK", "SOXX",  # Tech & Innovation
    "XLE", "XME",   # Energy & Materials
    "GLD", "GDX",   # Precious Metals
    "BTC-USD", "ETH-USD",  # Crypto & Digital Assets
    "AGG", "IEF",   # Fixed Income
    "XLY", "XLP",   # Consumer
    "XLV", "XBI",   # Health & Biotech
    "VNQ", "XLU",   # Real Assets
    "DBA",          # Agriculture
    "BIL"           # Cash / Liquidity
]

print("Checking historical data availability for all tickers...")
print("=" * 80)

earliest_date = None
ticker_info = []

for ticker in TICKERS:
    try:
        # Download max available history
        data = yf.download(ticker, period="max", progress=False)

        if not data.empty:
            start_date = data.index[0].strftime("%Y-%m-%d")
            end_date = data.index[-1].strftime("%Y-%m-%d")
            num_days = len(data)

            ticker_info.append({
                'ticker': ticker,
                'start': start_date,
                'end': end_date,
                'days': num_days
            })

            # Track earliest common date
            if earliest_date is None or data.index[0] > earliest_date:
                earliest_date = data.index[0]

            print(f"{ticker:10s} | Start: {start_date} | End: {end_date} | Days: {num_days:5d}")
        else:
            print(f"{ticker:10s} | NO DATA AVAILABLE")
            ticker_info.append({
                'ticker': ticker,
                'start': 'N/A',
                'end': 'N/A',
                'days': 0
            })
    except Exception as e:
        print(f"{ticker:10s} | ERROR: {e}")
        ticker_info.append({
            'ticker': ticker,
            'start': 'ERROR',
            'end': 'ERROR',
            'days': 0
        })

print("=" * 80)
print(f"\nRecommended safe start date (latest first date): {earliest_date.strftime('%Y-%m-%d') if earliest_date else 'N/A'}")
print(f"This ensures all tickers have data available from this point forward.")

# Find tickers with limited history
print("\n" + "=" * 80)
print("Tickers with limited history (started after 2010):")
for info in ticker_info:
    if info['start'] != 'N/A' and info['start'] != 'ERROR':
        year = int(info['start'].split('-')[0])
        if year > 2010:
            print(f"  {info['ticker']:10s} | Starts: {info['start']}")
