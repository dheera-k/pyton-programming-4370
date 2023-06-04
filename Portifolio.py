"""
            Author:       Dheera Joel Kanikella
            Date created: 06/03/2023
            Functionality: This program demonstrates reads files from Lesson6_Data_Stocks and Lesson6_Data_Bonds, AllStocks Json from calling API module
                        uses exception handling, changing datatypes, and writing the performance/portifolio
                        into a Stocks and Bonds DATABASE tables such as stocks, bonds, allstocks etc
                        which later the tables will be used as input for analysis
"""


import Stocks_Bonds_Classes as invest
import Stocks_API_Yahoo as api_allstocks
import os
import random
from datetime import datetime
import csv
import pandas as pd
import sqlite3
import json

# this import will run the API and generates AllStocks.json file
api_allstocks.main()

#Read both Stocks and Bonds files form the csv with Exception handling

def read_file(file_path):
    """
    Reads the input files ex: stocks and bonds from text files and converts to required input format
    for the classes and methods defined
    """
    try:
        with open(file_path, 'r') as fileobj:
            stock_info_lst = []
            for line in fileobj.readlines():
                stock_info_lst.append(line)
                
            stock_info = []
            header = stock_info_lst[0].strip().split(',')
            for value in stock_info_lst[1:]:
                values = value.strip().split(',')
                stock_info.append({header[i]: values[i] for i in range(len(header))})
            return stock_info
    except FileNotFoundError:
        raise Exception("The file to read doesn't exist, please check the file path")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {str(e)}")
    
def read_all_stocks(file_path):
    """
    Function to Read the input files json (AllStocks.json) using json import
    """
    try:
        with open(file_path, 'r') as fileobj:
            allstocks = json.load(fileobj)
            return allstocks
    except FileNotFoundError:
        raise Exception("The file doesn't exist, please check the file path")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {str(e)}")
    

#Write both Stocks and Bonds files using the csv module with Exception handling
def write_file(file_path, out_file):
    """
    Writes the output investor portifolio(s) into a file 
    """
    try:
    # get the list of headers for csv
        headers = list(out_file[0].keys())
        # Write the values into row lines
        with open(file_path, mode = 'w', newline ='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = headers)
            writer.writeheader()
            for row in out_file:
                writer.writerow(row)
    except FileNotFoundError:
        raise Exception("The file doesn't exist, please check the file path")
    except Exception as e:
         raise Exception(e)
    

# please change directory per your os by using command cd to run in the proper directory
working_directory = os.getcwd()


# creating/generating list of file paths to read
file_paths = []
file_path_stocks = working_directory + '/' + 'Lesson6_Data_Stocks.csv'
file_path_bonds = working_directory + '/' + 'Lesson6_Data_Bonds.csv'

file_paths.append(file_path_stocks)
file_paths.append(file_path_bonds)


# call the read function to read csv file
for file_path in file_paths:
    data = read_file(file_path)
    if 'Stocks' in file_path.split('/')[-1]:
        stock_info = data
    elif 'Bonds' in file_path.split('/')[-1]:
        bonds_info = data


############# Classes Instantiation ############
# Stocks Class - Performance
# using exception handling to raise issues when the inputs from csv is a string
# instead of number or float or while converting string to a date data type
# In-addition, the datatype changes are applied/reflected to the input read file so the datatypes are clean

# Stocks Class
for i, stock in enumerate(stock_info):
    stock_name = stock['SYMBOL']
    try:
        NO_SHARES = int(stock_info[i]['NO_SHARES'])
        stock_info[i]['NO_SHARES'] = NO_SHARES
        CURRENT_VALUE = float(stock_info[i]['CURRENT_VALUE'])
        stock_info[i]['CURRENT_VALUE'] = CURRENT_VALUE
        PURCHASE_PRICE = float(stock_info[i]['PURCHASE_PRICE'])
        stock_info[i]['PURCHASE_PRICE'] = PURCHASE_PRICE
        PURCHASE_DATE = datetime.strptime(stock_info[i]['PURCHASE_DATE'], '%m/%d/%Y').date()
        stock_info[i]['PURCHASE_DATE'] = PURCHASE_DATE
    except TypeError as e:
        raise Exception("An error occurred while processing the stock information:", e)
    
    purchaseid = random.randint(1,100)
    #initiating stock class
    myStocks = invest.Stock(stock_name, NO_SHARES, CURRENT_VALUE, PURCHASE_PRICE, PURCHASE_DATE, purchaseid)
    loss_or_gain = myStocks.Calculate_lossorgain()
    Percentage_yield_loss = myStocks.Percentage_yield_loss_func()
    yearlyearnings_loss = myStocks.Yearlyearnings_loss()

    stock_info[i]['Earnings_Loss'] = loss_or_gain
    # stock_info[i]['Percentage Yield/Loss'] = Percentage_yield_loss
    stock_info[i]['Yearly_Earning_Loss'] = yearlyearnings_loss


# Bond Class - Performance
# using exception handling to raise issues when the inputs from csv is a string
# instead of number or float or while converting string to a date data type
# In-addition, the datatype changes are applied/reflected to the input read file so the datatypes are clean

for i, bond in enumerate(bonds_info):
    stock_name = bond['SYMBOL']
    try:
        NO_SHARES = int(bond['NO_SHARES'])
        bonds_info[i]['NO_SHARES'] = NO_SHARES
        CURRENT_VALUE = float(bond['CURRENT_VALUE'])
        bonds_info[i]['CURRENT_VALUE'] = CURRENT_VALUE
        PURCHASE_PRICE = float(bond['PURCHASE_PRICE'])
        bonds_info[i]['PURCHASE_PRICE'] = PURCHASE_PRICE
        PURCHASE_DATE = datetime.strptime(bond['PURCHASE_DATE'], '%m/%d/%Y').date()
        bonds_info[i]['PURCHASE_DATE'] = PURCHASE_DATE
    except TypeError as e:
        raise Exception("An error occurred while processing the bond information:", e)
    
    purchaseid = random.randint(1,100)
    coupon = bond['Coupon']
    yield_rate = bond['Yield']

    #initiating Bond Class
    myBonds = invest.Bond(stock_name, NO_SHARES, CURRENT_VALUE, PURCHASE_PRICE, PURCHASE_DATE, purchaseid, coupon , yield_rate)
    loss_or_gain = myBonds.Calculate_lossorgain()
    Percentage_yield_loss = myBonds.Percentage_yield_loss_func()
    yearlyearnings_loss = myBonds.Yearlyearnings_loss()

    bonds_info[i]['Earnings_Loss'] = loss_or_gain
    # bonds_info[i]['Percentage Yield/Loss'] = Percentage_yield_loss
    bonds_info[i]['Yearly_Earning_Loss'] = yearlyearnings_loss
# print(bonds_info)


# Investor Class
investor_id = 'ID_' + str(random.randint(500,1000))
investor = invest.Investor(investor_id, 'Bob Smith', '123-456-7890')
investor.address = invest.Address('123 st', 'Denver', 'Colorado')
investor.stocks = stock_info
investor.bonds = bonds_info

# # following commented code is not required
# # As there is no create and replace command in sqlite 
# # I am using folloing to to drop tables and create them as I execute this code multiple times
# conn = sqlite3.connect('Investor.db')
# cursor = conn.cursor()
# conn.execute("DROP TABLE stocks")
# conn.execute("DROP TABLE bonds")
# conn.execute("DROP TABLE AllStocks")
# cursor.close()
# conn.close()


# Creating a Database, Tables and inserting into tables
try:
    conn = sqlite3.connect('Investor.db')
    cursor = conn.cursor()

    # Table for Stocks
    stock_col_headers = list(stock_info[0].keys())    
    #adding investor_id field to col headers
    stock_col_headers.append('INVESTOR_ID')
    # Create a table using the bond keys as column names
    column_names_stocks = ', '.join([f"{key} TEXT" for key in stock_col_headers])
    create_table_query_stocks = f"CREATE TABLE IF NOT EXISTS stocks ({column_names_stocks})"
    conn.execute(create_table_query_stocks)

    insert_query_stocks = "INSERT INTO stocks VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    for stock in stock_info:
        values = (
            stock['SYMBOL'],
            stock['NO_SHARES'],
            stock['PURCHASE_PRICE'],
            stock['CURRENT_VALUE'],
            stock['PURCHASE_DATE'],
            stock['Earnings_Loss'],
            stock['Yearly_Earning_Loss'],
            investor.investor_id
        )
        conn.execute(insert_query_stocks, values)

except sqlite3.Error as e:
    print("An error connecting or while using sqlite3:", e)



# Table for Bonds
bond_col_headers = list(bonds_info[0].keys())
#adding investor_id field to col headers
bond_col_headers.append('INVESTOR_ID')

# Create a table using the bond keys as column names
column_names_bonds = ', '.join([f"{key} TEXT" for key in bond_col_headers])
create_table_query_bonds = f"CREATE TABLE IF NOT EXISTS bonds ({column_names_bonds})"
conn.execute(create_table_query_bonds)

try:
    sql = "INSERT INTO bonds VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    # Insert data into the 'bonds' table
    for bond in bonds_info:
        values = (
            bond['SYMBOL'],
            bond['NO_SHARES'],
            bond['PURCHASE_PRICE'],
            bond['CURRENT_VALUE'],
            bond['PURCHASE_DATE'],
            bond['Coupon'],
            bond['Yield'],
            bond['Earnings_Loss'],
            bond['Yearly_Earning_Loss'],
            investor.investor_id
        )
        # Execute the query with the values
        cursor.execute(sql, values)
except sqlite3.Error as e:
    print("An error connecting or while using sqlite3:", e)


# # Table for AllStocks
file_path_allstocks = working_directory + '/' + 'AllStocks.json'
# read using the function defined
all_stocks = read_all_stocks(file_path_allstocks)
all_stocks_col_headers = list(all_stocks[0].keys())

# Create a table using the bond keys as column names
column_names_allstocks = ', '.join([f"{key} TEXT" for key in all_stocks_col_headers])
create_table_query_allstocks = f"CREATE TABLE IF NOT EXISTS AllStocks ({column_names_allstocks})"
conn.execute(create_table_query_allstocks)

try:
    # sql = "INSERT INTO bonds VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    sql = '''
    INSERT INTO AllStocks (Symbol, Date, Open, High, Low, Close, Volume)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    '''

    for item in all_stocks:
        values = (
            item['Symbol'],
            item['Date'],
            item['Open'],
            item['High'],
            item['Low'],
            item['Close'],
            item['Volume']
        )
        conn.execute(sql, values)
except sqlite3.Error as e:
    print("An error connecting or while using sqlite3:", e)


# Read for database tables and print the output in the tables
df_bonds = pd.read_sql_query("SELECT * FROM bonds", conn)
df_stocks = pd.read_sql_query("SELECT * FROM stocks", conn)
df_allstocks = pd.read_sql_query("SELECT * FROM AllStocks", conn)
# Commit and Close the database cursor and connection
conn.commit()
cursor.close()
conn.close()

# calling InvestorPortifolio class to print Investor Stocks and Bonds Performance from database input
investorPortifolio = invest.InvestorPortifolio()
investorPortifolio.print_portifolio(investor, df_stocks, 'Stock')
investorPortifolio.print_portifolio(investor, df_bonds, 'Bond')