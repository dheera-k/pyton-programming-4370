"""
            Author:       Dheera Joel Kanikella
            Date created: 06/04/2023
            Functionality: This program demonstrates analysis of Bob stocks compared to the market data
            This analyzes using a line chart for the trend of Bob's stocks performance over time
            Using Pandas for Data Manipulation and Matplotlib lib for Visualization
"""

# For sake of modularity and clarity I've defined classes in Stocks_Bonds_Classes.py, read files and Database loading in 'Portifolio.py' and visualization in this python file
# Where I used the classes are used to calculate portifolio from the input CSV, JSON files and stored the portiflio into a sqlite3 database tables
# I'll be reading the portiflio stocks table here to analyze with 'AllStocks.json'
# please note we are using GOOGL stock as 25 until now but in the Lesson6 CSV it is mistyped as 125. For better chart representation and to match with your output edited to 25

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sqlite3


# Read table such as Stocks input from the database 'Investor.db' and tables we saved in python file 'Portifolio.py'
def read_tables_from_db(table):
    """
    Function to read the stock protiflio loaded into sqlite3 Database tables under 'Investor.db'
    """
    try:
        conn = sqlite3.connect('Investor.db')
        df_stocks = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        return df_stocks
    except Exception as e:
        print("An error connecting or while using sqlite3:", e)

# read our stocks from the inserted table 
df_stocks = read_tables_from_db('stocks')
df_stocks['NO_SHARES'] = df_stocks['NO_SHARES'].astype('int') # changing data type for proper int multiplication later

# read AllStocks data from the inserted table in Portifolio.py
allstocks = read_tables_from_db('AllStocks')
df_allstocks = pd.DataFrame(allstocks)


# Identified GOOGL in our stocks and bonds portifolio is represented as GOOG in 'AllStocks.json', so renaming for proper join
df_allstocks['Symbol'].unique()
# df_allstocks['Symbol'].replace('GOOG', 'GOOGL', inplace = True) #used for week8 to make correction in the source file
df_allstocks['Symbol'].replace('SHEL', 'RDS-A', inplace = True) # Yahoo API doesn't have RDS-A so used equivalent Shell symbol and renamed
df_allstocks['Symbol'].replace('META', 'FB', inplace = True) # As Facebook changed to META, renaming to FB back just to align with previous assignments

# inner join to df_allstocks to get the number of shares Bob own and ignore the rest
df_join = pd.merge(df_allstocks, df_stocks, left_on='Symbol', right_on='SYMBOL', how='inner')
df_join['Close'] = df_join['Close'].replace('-', np.nan)
df_join['Close'] = df_join['Close'].astype(float)
df_join['Date'] = pd.to_datetime(df_join['Date'])
# df_join['Date'] = pd.to_datetime(df_join['Date'], format="%d-%b-%y")
df_join['stock_day_value'] = df_join['Close'] * df_join['NO_SHARES']
# print(df_join)


# Creating a line Graph after the join and multiplicaton
df_join = df_join.sort_values('Date', ascending=True) #sort to display in ascending

# Increase figure size and DPI
fig, ax = plt.subplots(figsize=(12, 8), dpi=100)

# creating the plot
for symbol in df_join['Symbol'].unique():
    df = df_join[df_join['Symbol'] == symbol]
    ax.plot(df['Date'], df['stock_day_value'], label=symbol)
    
plt.xlabel('Date')
plt.ylabel('Stock Day Value')
plt.title('Stock Day Value over Time')
plt.legend()
# plt.show()

plt.savefig('Stock_analysis_3year_trend.png')
