import datagrabber as dg
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

'''
Notes:
-Make chart look nicer
-Allow multiple tickers/portfolio to be charted and show legend
-show more prices on y axis
'''

#setting default to plot 100 days of data
DATAPOINTS = 100

def simplechart(symbol, datapoints=DATAPOINTS):
    #grabbing data for symbol
    data_df = dg.dailydata(symbol)

    #shortening df to as many requested data points and reversing order
    plot_df = pd.DataFrame(data_df["4. close"].iloc[:datapoints])
    plot_df = plot_df.iloc[::-1]

    print(plot_df.head()) #testing
    fig, ax = plt.subplots()
    ax.plot(plot_df) #plotting our data

    #formatting dates
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter('%y-%m-%d')

    ax.set_title(f'{symbol}')
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")

    plt.show()


if __name__ == "__main__":
    pass
