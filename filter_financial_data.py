import pandas as pd

def filter_financial_data(input_file: str, output_file: str, total_revenue: float, net_income: float, nitr: float, market_cap: float, fcf: float, eps: float) -> None:
    """
    Filters rows in the financial data CSV file based on the given criteria:
    - Total Revenue > total_revenue
    - Net Income > net_income
    - Net Income to Total Revenue Ratio > nitr
    - Market Cap > market_cap
    - Free Cash Flow > fcf
    - EPS > eps

    Writes the filtered results to an output CSV file.

    :param input_file: Path to the input CSV file containing financial data.
    :param output_file: Path to the output CSV file for storing filtered results.
    :param total_revenue: Total Revenue threshold.
    :param net_income: Net Income threshold.
    :param nitr: Net Income to Total Revenue Ratio threshold.
    :param market_cap: Market Cap threshold.
    :param fcf: Free Cash Flow threshold.
    :param eps: EPS threshold.
    """

    # Load data into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Apply the filters on the columns
    filtered_df = df[
        (df['Total Revenue'] > total_revenue) &
        (df['Net Income'] > net_income) &
        (df['Net income to total revenue ratio'] > nitr) &
        (df['Market Cap'] > market_cap) &
        (df['Free Cash Flow'] > fcf) &
        (df['EPS'] > eps)
    ]

    # Write the filtered data to the output CSV file
    if not filtered_df.empty:
        filtered_df.to_csv(output_file, index=False)
        print(f"Filtered data has been written to {output_file}.")
    else:
        print("No data met the criteria.")

# Example Usage
filter_financial_data('financial_data.csv', 'filtered_financial_data.csv', 0, 0, 0.05, 5_000_000_000, 0, 20.0)
