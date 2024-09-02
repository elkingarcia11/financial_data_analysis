import yfinance as yf
import csv
from typing import List, Dict

class FinancialData:
    def __init__(self, ticker_symbol: str):
        self.ticker_symbol = ticker_symbol
        self.ticker = yf.Ticker(self.ticker_symbol)
        self.quarterly_financials = self.ticker.quarterly_financials
        self.ttm_total_revenue = self.get_total_revenue()
        self.ttm_net_income = self.get_net_income()
        self.net_income_to_total_revenue_ratio = self.get_net_income_to_total_revenue_ratio()
        self.market_cap = self.get_market_cap()
        self.free_cash_flow = self.get_free_cash_flow()

    def get_total_revenue(self) -> float:
        """
        Fetches the trailing twelve months (TTM) total revenue for the given ticker symbol.

        :return: TTM total revenue or 0.0 if not available
        """
        try:
            total_revenue_quarters = self.quarterly_financials.loc['Total Revenue']
            ttm_total_revenue = total_revenue_quarters.head(4).sum()
            print("TTM Total Revenue:", ttm_total_revenue)
            return ttm_total_revenue
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error fetching total revenue for {self.ticker_symbol}: {e}")
            return 0.0

    def get_net_income(self) -> float:
        """
        Fetches the trailing twelve months (TTM) net income for the given ticker symbol.

        :return: TTM net income or 0.0 if not available
        """
        try:
            net_income_quarters = self.quarterly_financials.loc['Net Income']
            ttm_net_income = net_income_quarters.head(4).sum()
            print("TTM Net Income:", ttm_net_income)
            return ttm_net_income
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error fetching net income for {self.ticker_symbol}: {e}")
            return 0.0

    def get_net_income_to_total_revenue_ratio(self) -> float:
        """
        Calculates the ratio of net income to total revenue.

        :return: Ratio of net income to total revenue or 0.0 if total revenue is zero
        """
        if self.ttm_total_revenue == 0:
            print("Warning: Total revenue is zero, cannot calculate ratio.")
            return 0.0

        ratio = self.ttm_net_income / self.ttm_total_revenue
        print("Net Income to Total Revenue Ratio:", ratio)
        return ratio

    def get_market_cap(self) -> float:
        """
        Fetches the market capitalization for the given ticker symbol.

        :return: Market capitalization or 0.0 if not available
        """
        try:
            info = self.ticker.info
            market_cap = info.get('marketCap', 0.0)
            print(f"Market Capitalization of {self.ticker_symbol}: ${market_cap:,}")
            return market_cap
        except Exception as e:
            print(f"Error fetching market cap for {self.ticker_symbol}: {e}")
            return 0.0

    def get_free_cash_flow(self) -> float:
        """
        Fetches the latest Free Cash Flow for the given ticker symbol.

        :return: Latest Free Cash Flow value or 0.0 if not available
        """
        try:
            cash_flow = self.ticker.cashflow
            # Checking if the cash flow data is empty or missing
            if cash_flow.empty:
                print(f"No cash flow data available for ticker '{self.ticker_symbol}'")
                return 0.0
            # Check if 'Free Cash Flow' is in the cash flow data
            if "Free Cash Flow" in cash_flow.index:
                free_cash_flow = cash_flow.loc["Free Cash Flow"].iloc[0]
                print(f"Free Cash Flow for {self.ticker_symbol}: {free_cash_flow}")
                return free_cash_flow
            else:
                print(f"Free Cash Flow data not available for ticker '{self.ticker_symbol}'")
                return 0.0
        except Exception as e:
            print(f"Error fetching Free Cash Flow for ticker '{self.ticker_symbol}': {e}")
            return 0.0

    def to_dict(self) -> Dict[str, float]:
        """
        Converts the instance data to a dictionary suitable for CSV writing.

        :return: Dictionary containing the financial data
        """
        return {
            'Ticker': self.ticker_symbol,
            'Total Revenue': self.ttm_total_revenue,
            'Net income': self.ttm_net_income,
            'Net income to total revenue ratio': self.net_income_to_total_revenue_ratio,
            'Market Cap': self.market_cap,
            'Free Cash Flow': self.free_cash_flow
        }

    @staticmethod
    def write_header_if_needed(filename: str, headers: List[str]) -> None:
        """
        Writes the header to the CSV file if it does not already exist.

        :param filename: The name of the CSV file.
        :param headers: The list of column headers.
        """
        try:
            file_exists = False
            with open(filename, mode='r') as file:
                file_exists = True
        except FileNotFoundError:
            pass  # File does not exist, header will be written

        if not file_exists:
            with open(filename, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()

    def append_to_csv(self, filename: str = 'financial_data.csv') -> None:
        """
        Appends the instance data to the CSV file.

        :param filename: The name of the CSV file (default is 'financial_data.csv').
        """
        headers = ['Ticker', 'Total Revenue', 'Net income', 'Net income to total revenue ratio', 'Market Cap', 'Free Cash Flow']
        self.write_header_if_needed(filename, headers)

        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writerow(self.to_dict())

def read_tickers_from_csv(input_filename: str) -> List[str]:
    """
    Reads ticker symbols from a CSV file.

    :param input_filename: The name of the CSV file containing the ticker symbols.
    :return: A list of ticker symbols.
    """
    tickers = []
    try:
        with open(input_filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tickers.append(row['Ticker'])
        print(f"Successfully read {len(tickers)} tickers from {input_filename}")
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred while reading '{input_filename}': {e}")

    return tickers

def process_tickers(input_filename: str, output_filename: str) -> None:
    """
    Processes each ticker symbol and appends financial data to a CSV file.

    :param input_filename: The name of the CSV file containing the ticker symbols.
    :param output_filename: The name of the CSV file to append financial data to.
    """
    tickers = read_tickers_from_csv(input_filename)
    
    for ticker_symbol in tickers:
        try:
            financial_data = FinancialData(ticker_symbol)
            financial_data.append_to_csv(filename=output_filename)
            print(f"Processed {ticker_symbol}")
        except Exception as e:
            print(f"Error processing {ticker_symbol}: {e}")

# Example usage:
# process_tickers('tickers.csv', 'financial_data.csv')
