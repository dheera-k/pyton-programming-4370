"""
            Author:       Dheera Joel Kanikella
            Date created: 06/01/2023
            Functionality: This program demonstrates retreiving data from Stocks API 
                        for real-time performance analysis by comparing to Bob's portifolio.
                        This replaces "AllStocks.json" and used as a real-time data for the analysis.
                        Uses yahoo library and formats the data into the structure we have in previous assignment.
"""


# To install the library use pip
# pip install yfinance
# I've tried using www.alphavantage.co abd it's free API key, due to its limitations using Yahoo API

import json
import yfinance as yf
import pandas as pd


def stocks_from_api(symbols):
    data_list = []
    for stock_ticker in symbols:
        try:
            # Get latest trading day
            stock = yf.Ticker(stock_ticker)
            latest_trading_day = stock.history().index[-1].strftime('%Y-%m-%d')

            # Calculate the start and end dates for the three-year trailing period
            end_date = latest_trading_day
            start_date = (pd.to_datetime(end_date) - pd.DateOffset(years=3)).strftime('%Y-%m-%d')

            # Get historical stock data
            historical_data = stock.history(start=start_date, end=end_date)

            for date, values in historical_data.iterrows():
                entry = {
                    "Symbol": stock_ticker,
                    "Date": date.strftime('%Y-%m-%d'),
                    "Open": values['Open'],
                    "High": values['High'],
                    "Low": values['Low'],
                    "Close": values['Close'],
                    "Volume": values['Volume']
                }
                data_list.append(entry)
        except Exception as e:
            print(f"Error occurred for {stock_ticker}: {e}")
    return data_list

def save_api_stocks_json(data_list):
    # Saving the list of stock to a JSON file (AllStocks.json) that will be used as real-time input to Database
    try:
        with open('AllStocks.json', 'w') as file:
            json.dump(data_list, file)
            print("Successfully saved data to 'AllStocks.json'")
    except Exception as e:
        print(f"Error occurred while saving data to 'AllStocks.json': {e}")


def main():  
    symbols = ['GOOGL', 'MSFT', 'SHEL', 'AIG', 'META', 'M', 'F', 'IBM']
    data_output_list = stocks_from_api(symbols)
    save_api_stocks_json(data_output_list)

main()