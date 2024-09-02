# Financial Data Analysis

This project fetches and processes financial data for stock ticker symbols using the `yfinance` library. It retrieves key financial metrics such as total revenue, net income, market capitalization, and free cash flow. The data is then saved into a CSV file for further analysis.

## Features

- Fetches the trailing twelve months (TTM) total revenue and net income.
- Calculates the net income to total revenue ratio.
- Retrieves market capitalization and free cash flow.
- Reads ticker symbols from an input CSV file.
- Writes processed financial data to an output CSV file.

## Prerequisites

- Python 3.x
- `yfinance` library
- `csv` library (comes with Python)

## Installation

1. **Clone the repository** (if applicable) or download the source code.

2. **Install the `yfinance` library** using pip:

```bash pip install yfinance```

## Usage

1. Prepare the Input CSV File:
Create a CSV file named tickers.csv (or any name you prefer) containing a list of stock ticker symbols. The file should have a column named Ticker, like this:
    ```
    Ticker
    AAPL
    GOOGL
    MSFT
    ```

2. Run the Script
You can run the script using the following command, replacing tickers.csv with your input file and financial_data.csv with your desired output file name:

```bash python financial_data_analysis.py```

Or use the example function call provided at the bottom of the script:

```process_tickers('tickers.csv', 'financial_data.csv')```

3. Output
The script generates a CSV file (financial_data.csv by default) containing the financial data for each ticker symbol. The output file will have the following columns:

- Ticker
- Total Revenue
- Net income
- Net income to total revenue ratio
- Market Cap
- Free Cash Flow

## Code Overview

`FinancialData` class: Handles fetching and processing financial data for a single ticker symbol.

- `get_total_revenue()`: Retrieves the TTM total revenue.
- `get_net_income()`: Retrieves the TTM net income.
- `get_net_income_to_total_revenue_ratio()`: Calculates the ratio of net income to total revenue.
- `get_market_cap()`: Retrieves the market capitalization.
- `get_free_cash_flow()`: Retrieves the latest free cash flow value.
- `to_dict()`: Converts financial data to a dictionary format.
- `write_header_if_needed()`: Writes a CSV header if it doesn't exist.
- `append_to_csv()`: Appends financial data to the output CSV file.
- `read_tickers_from_csv()` function: Reads a list of ticker symbols from an input CSV file.

`process_tickers()` function: Processes each ticker symbol, fetches financial data, and appends it to the output CSV file.

## Error Handling
- If a ticker symbol's data is not available or if an error occurs during data retrieval, the script prints an error message and continues processing the next ticker symbol.
