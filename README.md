# Financial Data Processing Script

This project retrieves financial data for a list of stock tickers from Yahoo Finance using the `yfinance` library and saves it to a CSV file. It checks if data already exists and only fetches data that is missing or out-of-date.

## Project Structure

- **tickers.csv**: Contains a list of stock tickers to retrieve data for.
- **financial_data.csv**: Stores the financial data of each ticker including Total Revenue, Net Income, Net income to total revenue ratio, Market Cap, Free Cash Flow, and EPS.
- **financial_data.py**: Python script to fetch, process, and save the financial data.
- **filter_financial_data.py**: Python script to filter and output financial data based on provided thresholds.
- **requirements.txt**: Lists the required Python packages for this project.

## CSV File Format

### tickers.csv
| Ticker |
|--------|
| A      |
| AA     |
| ...    |

### financial_data.csv
| Ticker | Total Revenue | Net Income | Net income to total revenue ratio | Market Cap | Free Cash Flow | EPS |
|--------|---------------|------------|-----------------------------------|------------|----------------|-----|
| A      | ...           | ...        | ...                               | ...        | ...            | ... |
| AA     | ...           | ...        | ...                               | ...        | ...            | ... |
| ...    | ...           | ...        | ...                               | ...        | ...            | ... |

## Installation

1. Clone the repository to your local machine.
2. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Fetching Financial Data

1. **Prepare `tickers.csv`:**  
   Add the stock tickers you want to process in `tickers.csv`. This file should contain a single column with the header `Ticker`.

2. **Run the script:**

```bash
python financial_data.py
```

This will fetch financial data for each ticker in `tickers.csv`, and save the results in `financial_data.csv`.

### Filtering Financial Data

1. **Filter financial data based on custom thresholds**  
   You can filter the data using the `filter_financial_data.py` script. This script allows you to specify threshold values for several metrics and outputs the filtered results to a CSV file.

2. **Run the filtering script:**

```bash
python filter_financial_data.py
```

Example:

```bash
python filter_financial_data.py financial_data.csv filtered_financial_data.csv 5000000000 1000000000 0.05 20000000000 1.0 5.0
```

This will filter rows from `financial_data.csv` where:
- Total Revenue > 5,000,000,000
- Net Income > 1,000,000,000
- Net Income to Total Revenue Ratio > 0.05
- Free Cash Flow > 1.0
- EPS > 5.0
- Market Cap > 20,000,000,000

## How it Works

1. **Read Tickers:** The script reads the list of stock tickers from `tickers.csv`.
2. **Fetch Financial Data:** For each ticker, it checks if data exists in `financial_data.csv`. If any required fields are missing, it fetches the data using `yfinance`.
3. **Save Financial Data:** The script appends the data for each ticker to `financial_data.csv`.

## Requirements

- **Python 3.7+**
- **Required Python Libraries:**

```
pandas
yfinance
```

## Notes

- This script only fetches financial data for tickers that are missing or have incomplete data in `financial_data.csv`.
- Supported financial metrics include:
  - Total Revenue (TTM)
  - Net Income (TTM)
  - Net Income to Total Revenue Ratio
  - Market Capitalization
  - Free Cash Flow
  - Earnings Per Share (EPS)