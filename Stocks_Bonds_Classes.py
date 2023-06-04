"""
            Author:       Dheera Joel Kanikella
            Date created: 05/10/2023
            Functionality: This program demonstrates Stocks of BOB and print their performance portifolio
                        using Classes, Object Orientation Programming using inheritance, Composition
"""

import datetime

# Investor class to generate details of the Investor who owns stocks/bonds
class Investor:
    def __init__(self, investor_id, name, phone_number):
        self.name = name
        self.investor_id = investor_id
        self.address = None
        self.phone_number = phone_number
        self.stocks = []
        self.bonds = []

# Address class used as a Composition in the Investor class
class Address():
    def __init__(self, street, city, state):
        self.street = street
        self.city = city
        self.state = state

    def __str__(self):
        lines = []
        lines.append(self.street)
        lines.append(self.city)
        lines.append(self.state)
        return ' '.join(lines)
    

# Stock Class to define stocks and calculates the loss or gain in the portifolio  
class Stock():
    def __init__(self, stock_name, numofshares, currentprice, purchaseprice, purchasedate, purchaseid):
        self.stock_name = stock_name
        self.numofshares = numofshares
        self.purchaseprice = purchaseprice
        self.currentprice = currentprice
        self.purchasedate = purchasedate
        self.purchaseID = purchaseid

    #Defining a function to calculate the loss/gain 
    def Calculate_lossorgain(self):
        earnings_loss = (self.currentprice - self.purchaseprice) * self.numofshares
        earnings_loss = round(earnings_loss, 2)
        return earnings_loss

    #Defining a second function
    def Percentage_yield_loss_func(self):
        Percentage_yield_loss = (self.currentprice - self.purchaseprice) / self.purchaseprice * 100
        Percentage_yield_loss = round(Percentage_yield_loss, 2)
        return Percentage_yield_loss
    
    #Defining a third function
    def Yearlyearnings_loss(self):    
        percentagechange = (self.currentprice - self.purchaseprice) / self.purchaseprice
        numberofdays = (datetime.date.today() - self.purchasedate).days
        returnrate = percentagechange / numberofdays
        annualizedreturn = returnrate * 365
        yearlyearnings_loss = annualizedreturn * 100
        yearlyearnings_loss=round(yearlyearnings_loss, 2)
        return yearlyearnings_loss
  
    
# Bond Class to define bonds and calculates the loss or gain in the portifolio
class Bond(Stock):
    def __init__(self, stock_name, numofshares, currentprice, purchaseprice, purchasedate, purchaseid, coupon, yield_rate):
        super().__init__(stock_name, numofshares, currentprice, purchaseprice, purchasedate, purchaseid)
        self.coupon = coupon
        self.yield_rate = yield_rate

    def get_coupon(self):
        return self.coupon
    
    def get_yield(self):
        return self.yield_rate 
    
    def Calculate_lossorgain(self):
        return super().Calculate_lossorgain()
    
    def Percentage_yield_loss_func(self):
        return super().Percentage_yield_loss_func()
    
    def Yearlyearnings_loss(self):
        return super().Yearlyearnings_loss()
    
# InvestorPortifolio to print the performance of stocks for the Investor
class InvestorPortifolio:
    def print_portifolio(self, investor, df, investment_type):
        print(f"\t\t\t {investment_type} ownership for {investor.name}")
        print(f"\t\t\tInvestor Address: {investor.address}")
        print('-' * 80)
        if investment_type == 'Stock':
            df = df[['INVESTOR_ID', 'SYMBOL', 'NO_SHARES', 'Earnings_Loss', 'Yearly_Earning_Loss']]
        elif investment_type == 'Bond':
            df = df[['INVESTOR_ID', 'SYMBOL', 'NO_SHARES', 'Earnings_Loss', 'Yearly_Earning_Loss', 'Coupon', 'Yield']]
        print(df)
        print('\n')

# Note: I was using Address an example for Composition. It doesn't have to be a different class, 
# I used as optional for investor to input the address if they are concerned they wouldn't need to input due to privacy. 