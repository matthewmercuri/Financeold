import datagrabber as dg
from datetime import date
import os
import pandas as pd
import time

def _benchmark():
    #follows logic of stockstats function
    _benchmark_df = dg.dailydata("SPX") #can use VTI as well
    _benchmark_df = _benchmark_df.iloc[::-1]
    pchange_df = _benchmark_df['4. close'].pct_change()
    _benchmark_df['P Change'] = pchange_df.apply(lambda x: x*100)

    return _benchmark_df



def _fetch_for_local_string_helper(symbols, filetype):
    #Times out if list is too long to avoid hitting API cap
    if len(symbols)>=5:
        timeout = 12
    else:
        timeout = 0

    for symbol in symbols:
        _fetch_for_local_helper(symbol, filetype)
        time.sleep(timeout)



def _fetch_for_local_helper(symbols, filetype):

    if isinstance(symbols, str) == True: #validating input as string
        _today = date.today()
        data = stockstats(symbols) #grabbing historical data
        if filetype == 'csv':
            data.to_csv('./StockData/'+f'{symbols}_{_today}.csv')
        elif filetype == 'xlsx':
            data.to_excel('./StockData/'+f'{symbols}_{_today}.xlsx')
        else:
            print('Please enter a valid filetype (.csv, .xlsx)!')
    else:
        print('Please enter a vaid list of strings')



def stockstats(symbol):
    #returns a df of all stock stats, including percent change for a given symbol
    #use this function to add columns, so calls for local storage include them
    stock_df = dg.dailydata(symbol) #returns a df of daily data
    stock_df = stock_df.iloc[::-1] #reverses order
    pchange_df = stock_df['4. close'].pct_change() #finds percent change
    stock_df['P Change'] = pchange_df.apply(lambda x: x*100) #multiplies by 100

    return stock_df



def beta(symbol, pastdays=1825):
    #returns the beta for any given ticker symbol
    stock_df = stockstats(symbol) #fetching stock data
    bench_df = _benchmark() #fetching benchmark data
    stock_df = stock_df.tail(pastdays) #trimming to desired recent length
    bench_df = bench_df.tail(pastdays) #default of 5 years

    cov = stock_df['P Change'].cov(bench_df['P Change']) #finding covariance
    var = bench_df['P Change'].var() #returning variance
    beta = float(cov) / float(var) #formula for beta

    return beta



def fetch_for_local(symbols, filetype='csv'):
    #create a directory to store historical stock data if it does not already exist
    try:
        os.mkdir("./StockData/")
    except OSError:
        print("Unable to create directory! (Perhaps already exists?)")
    else:
        print("Created directory!")

    if isinstance(symbols, list)==True: #check if the parameter is a list
        _fetch_for_local_string_helper(symbols, filetype)
    else:
        _fetch_for_local_helper(symbols, filetype)


if __name__ == "__main__":
    pass
