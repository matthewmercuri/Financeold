from bs4 import BeautifulSoup
from datetime import date
import json
import pandas as pd
import requests

"""
ALPHAVANTAGE API IS USED
www.alphantage.co
API Paramaters
function - data we need to pull: pricing, indicators, etc.
symbol - stock ticker symbol
outputsize - compact for 100 data points or full for 20+ years
datatype - json and csv are supported
apikey - assigned API key

limited to 5 calls per min/ 500 per day
"""

APIKEY = "MOCKAPIKEY" #our API Key
BASESTRING = "https://www.alphavantage.co/query?"



def dailydata(symbol, OUTPUTSIZE="full", FUNCTION="TIME_SERIES_DAILY_ADJUSTED",
              get_csv=False):
    #calling this function returns a df of a stocks price data

    #combining all values for string
    string_complete = f"{BASESTRING}function={FUNCTION}&symbol={symbol}&outputsize={OUTPUTSIZE}&apikey={APIKEY}"
    #print(string_complete) #testing
    r = requests.get(string_complete) #creating request object from URL
    raw_json = json.loads(json.dumps(r.json())) #generating json from request object and assigning it
    j = raw_json["Time Series (Daily)"] #selecting data from json

    df = pd.DataFrame(j) #creating a pandas df with json
    df = pd.DataFrame.transpose(df)
    df["4. close"] = df["4. close"].astype(float) #converting prices from str to float

    #creating a CSV of return data
    if get_csv==True:
        _today = date.today()
        df.to_csv(f"{symbol}_{_today}.csv")


    return df





def getsp500tickers(get_csv=False):
    #calling this function returns a list of all the sp500 constituents (strings)

    #link to wikipedia article listing sp500 constituents
    _sp500link = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    _r = requests.get(_sp500link) #creating requests object
    data = _r.text
    soup = BeautifulSoup(data, 'lxml') #passing requsts object for web scrape

    table = soup.find('table', {'class':'wikitable sortable'}) #selecting table
    table = table.prettify()
    tabledata = pd.read_html(table) #creating dataframes with table
    sp500df = pd.DataFrame(tabledata[0]) #selecting desired dataframe
    sp500df_tickers = sp500df[0]

    if get_csv == True:
        #if true, creates csv of constituents tickers
        _today = date.today()
        sp500df_tickers.to_csv(f"SP500Tickers_{_today}.csv")

    ticker_list = list((sp500df_tickers.to_dict()).values())
    ticker_list = ticker_list[1:]

    return ticker_list

if __name__ == "__main__":
    pass
