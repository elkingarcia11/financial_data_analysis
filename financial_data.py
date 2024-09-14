import yfinance as yf
import csv
from typing import List, Dict
import pandas as pd
from datetime import datetime

class FinancialData:
    def __init__(self, ticker_symbol: str, csv_row: Dict[str, str]):
        self.ticker_symbol = ticker_symbol
        self.csv_row = csv_row
        self.should_fetch_data = self.is_any_field_empty(csv_row)

        # Only initialize `yf.Ticker` if at least one field is missing
        if self.should_fetch_data:
            print(f"{ticker_symbol} data is out of date. Retrieving updates now...")
            self.ticker = yf.Ticker(self.ticker_symbol)
        else:
            print(f"{ticker_symbol} is up to date.")
            self.ticker = None  # Ticker initialization is skipped

        self.ttm_total_revenue = self.check_and_fetch_field('Total Revenue', self.get_total_revenue)
        self.ttm_net_income = self.check_and_fetch_field('Net Income', self.get_net_income)
        self.net_income_to_total_revenue_ratio = self.check_and_fetch_field('Net income to total revenue ratio', self.get_net_income_to_total_revenue_ratio)
        self.market_cap = self.check_and_fetch_field('Market Cap', self.get_market_cap)
        self.free_cash_flow = self.check_and_fetch_field('Free Cash Flow', self.get_free_cash_flow)
        self.eps = self.check_and_fetch_field('EPS', self.get_eps)
    
    def is_any_field_empty(self, csv_row: Dict[str, str]) -> bool:
        """
        Check if any required field is missing, NaN, or an empty string in the CSV row.
        """
        required_fields = ['Total Revenue', 'Net Income', 'Net income to total revenue ratio', 'Market Cap', 'Free Cash Flow', 'EPS']
        return any(pd.isna(csv_row.get(field)) or csv_row.get(field) == '' for field in required_fields)
        
    def check_and_fetch_field(self, field_name: str, fetch_func):
        """
        Checks if the given field is available in the CSV row. If not, fetches the data using the provided fetch function.

        :param field_name: The name of the field to check in the CSV row.
        :param fetch_func: The function to call to fetch the field's value if missing.
        :return: The field value from the CSV or the fetched value.
        """
        if field_name in self.csv_row and pd.notna(self.csv_row[field_name]):
            return float(self.csv_row[field_name])
        else:
            # Field is missing, so fetch it using the provided function
            return fetch_func()
        
    def get_total_revenue(self) -> float:
        try:
            quarterly_financials = self.ticker.quarterly_financials
            total_revenue_quarters = quarterly_financials.loc['Total Revenue']
            ttm_total_revenue = total_revenue_quarters.head(4).sum()
            return ttm_total_revenue
        except (KeyError, IndexError, TypeError) as e:
            return 0.0

    def get_net_income(self) -> float:
        try:
            quarterly_financials = self.ticker.quarterly_financials
            net_income_quarters = quarterly_financials.loc['Net Income']
            ttm_net_income = net_income_quarters.head(4).sum()
            return ttm_net_income
        except (KeyError, IndexError, TypeError) as e:
            return 0.0

    def get_net_income_to_total_revenue_ratio(self) -> float:
        if self.ttm_total_revenue == 0:
            return 0.0
        return self.ttm_net_income / self.ttm_total_revenue

    def get_market_cap(self) -> float:
        try:
            info = self.ticker.info
            return info.get('marketCap', 0.0)
        except Exception as e:
            return 0.0

    def get_free_cash_flow(self) -> float:
        try:
            cash_flow = self.ticker.cashflow
            if "Free Cash Flow" in cash_flow.index:
                return cash_flow.loc["Free Cash Flow"].iloc[0]
            else:
                return 0.0
        except Exception as e:
            return 0.0

    def get_eps(self) -> float:
        """
        Fetches the trailing twelve months (TTM) Earnings Per Share (EPS) for the given ticker symbol.

        :return: Trailing EPS or 0.0 if not available
        """
        try:
            eps = self.ticker.info['trailingEps']
            print(f"Trailing EPS for {self.ticker_symbol}: {eps}")
            return eps
        except Exception as e:
            print(f"Error fetching EPS for {self.ticker_symbol}: {e}")
            return 0.0

    def to_dict(self) -> Dict[str, float]:
        return {
            'Ticker': self.ticker_symbol,
            'Total Revenue': self.ttm_total_revenue,
            'Net Income': self.ttm_net_income,
            'Net income to total revenue ratio': self.net_income_to_total_revenue_ratio,
            'Market Cap': self.market_cap,
            'Free Cash Flow': self.free_cash_flow,
            'EPS': self.eps
        }

    @staticmethod
    def write_header_if_needed(filename: str, headers: List[str]) -> None:
        try:
            file_exists = False
            with open(filename, mode='r') as file:
                file_exists = True
        except FileNotFoundError:
            pass

        if not file_exists:
            with open(filename, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()

    def append_to_csv(self, filename: str = 'financial_data.csv') -> None:
        headers = ['Ticker', 'Total Revenue', 'Net Income', 'Net income to total revenue ratio', 'Market Cap', 'Free Cash Flow', 'EPS']
        self.write_header_if_needed(filename, headers)

        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writerow(self.to_dict())

    @classmethod
    def read_tickers_from_csv(cls, input_filename: str) -> List[Dict[str, str]]:
        try:
            df = pd.read_csv(input_filename)
            return df.to_dict('records')
        except FileNotFoundError:
            print(f"Error: File {input_filename} not found.")
            return []
        except Exception as e:
            print(f"An error occurred while reading {input_filename}: {e}")
            return []

    @classmethod
    def process_tickers(cls, input_filename: str, output_filename: str) -> None:
        data = cls.read_tickers_from_csv(input_filename)
        headers = ['Ticker', 'Total Revenue', 'Net Income', 'Net income to total revenue ratio', 'Market Cap', 'Free Cash Flow', 'EPS']
        
        for row in data:
            ticker_symbol = row.get('Ticker')
            if ticker_symbol:
                try:
                    financial_data = cls(ticker_symbol, row)
                    financial_data.append_to_csv(filename=output_filename)
                except Exception as e:
                    print(f"Error processing {ticker_symbol}: {e}")

if __name__ == '__main__':
    now = datetime.now()
    input_filename = 'tickers.csv'
    output_filename = f'financial_data{now.strftime("%Y-%m-%d")}.csv'
    FinancialData.process_tickers(input_filename, output_filename)
