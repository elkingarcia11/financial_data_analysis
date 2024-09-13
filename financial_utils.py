import pandas as pd
from financial_data import FinancialData

def append_eps_to_csv(input_filename: str, output_filename: str) -> None:
    """
    Reads the financial data from a CSV file, fetches the EPS for each ticker,
    and appends the EPS to the CSV file.
    
    :param input_filename: The name of the CSV file containing the financial data.
    :param output_filename: The name of the CSV file to write the updated data to.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(input_filename)
        
        # Add a new column for EPS
        df['EPS'] = None
        
        # Loop through the first 5 tickers and fetch the EPS
        for index, row in df.iterrows():
            ticker_symbol = row['Ticker']
            financial_data = FinancialData(ticker_symbol, row)
            df.at[index, 'EPS'] = financial_data.eps  # Update the EPS column for this ticker
            
        # Save the updated DataFrame to a new CSV file
        df.to_csv(output_filename, index=False)
        print(f"Successfully updated {len(df)} rows with EPS data and saved to {output_filename}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred while processing '{input_filename}': {e}")

# Example Usage:
# FinancialData.process_tickers('input_tickers.csv', 'output_financial_data.csv')

append_eps_to_csv("financial_data.csv", "new_data.csv")