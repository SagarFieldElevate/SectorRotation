# Historical Data Backfill Guide

This guide explains how to add historical data to your Sector Rotation Excel file.

## 📊 Data Availability

### Historical Data Timeline

| Ticker | Asset Type | Available From | Years of Data |
|--------|-----------|----------------|---------------|
| XLK | Tech ETF | ~1998 | 26+ years |
| SOXX | Semiconductor ETF | 2001 | 23+ years |
| XLE | Energy ETF | ~1998 | 26+ years |
| XME | Metals & Mining ETF | 2006 | 18+ years |
| GLD | Gold ETF | 2004 | 20+ years |
| GDX | Gold Miners ETF | 2006 | 18+ years |
| **BTC-USD** | **Bitcoin** | **2014** | **10+ years** |
| **ETH-USD** | **Ethereum** | **2017** | **7+ years** |
| AGG | Bond Aggregate ETF | 2003 | 21+ years |
| IEF | Treasury ETF | 2002 | 22+ years |
| XLY | Consumer Discretionary | ~1998 | 26+ years |
| XLP | Consumer Staples | ~1998 | 26+ years |
| XLV | Healthcare ETF | ~1998 | 26+ years |
| XBI | Biotech ETF | 2006 | 18+ years |
| VNQ | Real Estate ETF | 2004 | 20+ years |
| XLU | Utilities ETF | ~1998 | 26+ years |
| DBA | Agriculture ETF | 2007 | 17+ years |
| BIL | T-Bills ETF | 2007 | 17+ years |

### Recommended Start Dates

1. **Maximum History (2007)**: Use if you want maximum coverage for most assets
   - Missing: BTC-USD, ETH-USD (will show N/A for these sectors)
   - Best for: Traditional asset analysis

2. **All Assets Including Bitcoin (2017)**: Use if you want all sectors including crypto
   - Complete: All sectors have data
   - Best for: Comprehensive sector rotation including digital assets

3. **Recent History (2020+)**: Use for recent trend analysis
   - Complete: All sectors have data
   - Best for: Quick analysis of recent market behavior

## 🚀 Quick Start

### Option 1: Using yfinance (FREE)

```bash
# Install dependencies
pip install yfinance pandas openpyxl python-dateutil

# Backfill from 2017 (recommended - includes all crypto)
python backfill_historical_data.py 2017 1

# Or from 2020 (recent history only)
python backfill_historical_data.py 2020 1

# Or from 2010 (max history, crypto will be N/A)
python backfill_historical_data.py 2010 1
```

### Option 2: Using Twelve Data API

```bash
# Install dependencies
pip install twelvedata pandas openpyxl python-dateutil

# Set your API key
export TWELVEDATA_API_KEY="your_api_key_here"

# Backfill from 2017
python backfill_twelvedata.py 2017 1

# Or pass API key directly
python backfill_twelvedata.py 2017 1 --api-key your_api_key_here
```

## 📝 Usage Examples

### Example 1: Complete Backfill from 2017
```bash
python backfill_historical_data.py 2017 1
```
Output: Adds ~96 months of historical data (2017-01 to present)

### Example 2: Backfill Recent 3 Years
```bash
python backfill_historical_data.py 2021 1
```
Output: Adds ~48 months of historical data (2021-01 to present)

### Example 3: Backfill Specific Range
Edit the script to add end_year and end_month parameters, or it will automatically go to the previous complete month.

## 🔍 How It Works

The backfill scripts:

1. **Fetch Historical Prices**: Download end-of-month closing prices for each ticker
2. **Calculate Returns**: Compute month-over-month returns
3. **Apply Weights**: Calculate weighted returns for each sector basket
4. **Update Excel**: Insert data into the Excel file (preserves existing data)
5. **Identify Top Performers**: Automatically calculates Top #1 and Top #2 sectors

## ⚙️ Configuration

### Sector Baskets (from update_sector_returns.py)

```python
SECTORS = {
    "Tech & Innovation": [("XLK", 0.5), ("SOXX", 0.5)],
    "Energy & Materials": [("XLE", 0.5), ("XME", 0.5)],
    "Precious Metals": [("GLD", 0.6), ("GDX", 0.4)],
    "Crypto & Digital Assets": [("BTC-USD", 0.6), ("ETH-USD", 0.4)],
    "Fixed Income": [("AGG", 0.7), ("IEF", 0.3)],
    "Consumer": [("XLY", 0.6), ("XLP", 0.4)],
    "Health & Biotech": [("XLV", 0.6), ("XBI", 0.4)],
    "Real Assets": [("VNQ", 0.6), ("XLU", 0.4)],
    "Agriculture": [("DBA", 1.0)],
    "Cash / Liquidity": [("BIL", 1.0)],
}
```

## ⚠️ Important Notes

### Data Quality
- **Missing Data**: If a ticker has no data for a specific month, that sector will show "N/A"
- **Crypto Limitations**: Bitcoin data on Yahoo Finance starts ~2014, Ethereum ~2017
- **Weighted Calculations**: If any component is missing, the sector return is calculated using available components only

### API Limits
- **yfinance**: Free, but may have rate limits if fetching large amounts of data quickly
- **Twelve Data**: Free tier has limits (800 API calls/day for free tier)
- **Recommendation**: If you hit rate limits, add sleep delays between months

### Excel File
- **Preserves Existing Data**: The script won't duplicate data if you run it multiple times
- **Updates Existing Rows**: If a month already exists, it will update that row
- **Sorted by Date**: Rows are organized chronologically

## 🐛 Troubleshooting

### Issue: "No data available for ticker XYZ"
- **Cause**: Ticker doesn't have data for that time period
- **Solution**: Start from a more recent date or accept N/A for that sector

### Issue: "HTTP 403 / Rate limit exceeded"
- **Cause**: Too many API requests
- **Solution**:
  - Add delays: `time.sleep(0.5)` between months
  - Use smaller date ranges
  - Try Twelve Data API instead

### Issue: "Module not found"
- **Cause**: Missing dependencies
- **Solution**: `pip install yfinance pandas openpyxl python-dateutil`

## 📈 Expected Results

After running the backfill from 2017:

```
Year-Month | Tech & Innovation | Energy & Materials | ... | Top #1 | Top #2 | Avg Return %
2017-01    | 5.23             | 3.45               | ... | Tech   | Health | 3.89
2017-02    | 3.12             | -1.23              | ... | Tech   | Precious | 2.45
...
2024-10    | 4.56             | 2.34               | ... | Tech   | Consumer | 3.21
```

## 🎯 Recommended Workflow

1. **Backup your Excel file first**
   ```bash
   cp Field_Elevate_Sector_Monthly_Returns.xlsx Field_Elevate_Sector_Monthly_Returns_backup.xlsx
   ```

2. **Run backfill with test range** (e.g., 1 year)
   ```bash
   python backfill_historical_data.py 2023 1
   ```

3. **Verify the Excel file** looks correct

4. **Run full backfill**
   ```bash
   python backfill_historical_data.py 2017 1
   ```

5. **Commit changes**
   ```bash
   git add Field_Elevate_Sector_Monthly_Returns.xlsx
   git commit -m "Add historical sector returns from 2017"
   git push
   ```

## 🔧 Advanced: Modify the Script

To change the start date default in the script, edit line in `backfill_historical_data.py`:

```python
# Change from:
start_year = 2017
start_month = 1

# To (for example):
start_year = 2020
start_month = 1
```

## 📞 Support

If you encounter issues:
1. Check the error messages in console output
2. Verify your internet connection (required for data download)
3. Ensure API keys are set correctly (for Twelve Data)
4. Try with a smaller date range first
