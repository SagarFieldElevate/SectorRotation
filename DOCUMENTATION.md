# SectorRotation Application Documentation

## 1. WHAT IT DOES

This application calculates and records monthly investment returns for 10 predefined sectors. It downloads historical price data from financial markets, computes weighted percentage returns for each sector based on a basket of tickers, identifies the two best-performing sectors, calculates the average return across all sectors, and stores these results in an Excel spreadsheet.

The application updates a single Excel file (`Field_Elevate_Sector_Monthly_Returns.xlsx`) by adding or updating a row for the previous month with calculated return percentages.

## 2. WHY IT EXISTS

The application exists to maintain an automated, historical record of sector performance for Field Elevate's investment strategy. It eliminates manual data collection and calculation by automatically fetching market data and computing sector returns on a monthly schedule. The stored data provides a time-series record spanning multiple years (currently 102 rows of historical data) for tracking sector rotation patterns.

## 3. HOW IT WORKS

### Core Logic

The application executes the following process:

1. **Date Calculation**: Determines the previous month relative to the current UTC date
2. **Data Retrieval**: For each sector, downloads daily price data from Yahoo Finance for all constituent tickers
3. **Return Calculation**:
   - Extracts the last closing price (or adjusted close) of the target month
   - Extracts the last closing price of the preceding month
   - Calculates simple return: `(current_close / previous_close) - 1`
4. **Weighted Aggregation**: Combines multiple ticker returns within each sector using predefined weights
5. **Top Performers**: Identifies the two sectors with the highest returns
6. **Average Calculation**: Computes the mean return across all sectors
7. **Excel Update**: Writes or updates the row corresponding to the month in the Excel file

### Sector Definitions

The application tracks 10 sectors, each represented by 1-2 tickers with specific weights:

- **Tech & Innovation**: XLK (50%), SOXX (50%)
- **Energy & Materials**: XLE (50%), XME (50%)
- **Precious Metals**: GLD (60%), GDX (40%)
- **Crypto & Digital Assets**: BTC-USD (60%), ETH-USD (40%)
- **Fixed Income**: AGG (70%), IEF (30%)
- **Consumer**: XLY (60%), XLP (40%)
- **Health & Biotech**: XLV (60%), XBI (40%)
- **Real Assets**: VNQ (60%), XLU (40%)
- **Agriculture**: DBA (100%)
- **Cash / Liquidity**: BIL (100%)

### Excel Structure

The Excel file contains a worksheet named "Monthly" with the following columns:

1. Year-Month (format: YYYY-MM)
2. Notes (empty, manual entry field)
3. Ten sector return columns (percentage values)
4. Top #1 (name of best-performing sector)
5. Top #2 (name of second-best-performing sector)
6. Average Return % (mean of all sector returns)

The header row uses white text on blue background (color: #0056A3).

### Automation

A GitHub Actions workflow automates the entire process:

- **Workflow File**: `.github/workflows/update.yml`
- **Environment**: Ubuntu Latest with Python 3.11
- **Dependencies**: yfinance, pandas, openpyxl, python-dateutil
- **Execution**: Runs the Python script, commits updated Excel file, and pushes to repository
- **Git Configuration**: Uses "GitHub Actions" as committer with message format "Auto update YYYY-MM-DD"

## 4. DATA USED

### External Data Sources

1. **Yahoo Finance API** (via `yfinance` Python library)
   - Provides daily price data for 13 ETF tickers and 2 cryptocurrency pairs
   - Accessed for the target month and previous month to calculate returns
   - Specific data point used: "Adj Close" (if available) or "Close" price
   - Tickers: XLK, SOXX, XLE, XME, GLD, GDX, BTC-USD, ETH-USD, AGG, IEF, XLY, XLP, XLV, XBI, VNQ, XLU, DBA, BIL

### Internal Data Files

1. **Field_Elevate_Sector_Monthly_Returns.xlsx**
   - Stores cumulative historical monthly returns
   - Currently contains 102 rows of data (plus header)
   - Read at runtime to check for existing month entries
   - Written/updated after calculating new monthly returns
   - If missing, automatically created with formatted header row

### Configuration Data

Hardcoded in `update_sector_returns.py`:
- Sector names and ticker compositions with weights (lines 9-20)
- Excel file path (line 22)
- Column structure (line 21)

## 5. WHEN IT IS USED

### Scheduled Execution

The application runs automatically via GitHub Actions on:
- **Schedule**: 2nd day of every month at 6:00 AM UTC
- **Cron Expression**: `0 6 2 * *`

This timing ensures the previous month's data is available from financial markets before processing.

### Manual Execution

The workflow can be triggered manually through:
- GitHub Actions interface using `workflow_dispatch` trigger
- Local execution by running: `python update_sector_returns.py`

### Operational Context

The application operates in the following workflow:
1. Month completes and market data becomes available
2. GitHub Actions triggers on the 2nd of the following month
3. Script executes, fetches data, performs calculations
4. Excel file is updated with the previous month's returns
5. Changes are committed and pushed to the repository
6. Updated data is available for analysis or downstream use

The application does not run intraday or track real-time prices. It processes one month at a time, always targeting the completed previous month relative to the execution date.
