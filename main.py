import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ticker = ["SPY", "AAPL", "KO"]

stocks = yf.download(ticker, start = "2010-01-01", end = "2021-01-01")

stocks = pd.read_csv("stocksYT.csv", header = [0,1], index_col=[0], parse_dates=[0])

# convert multi index to tuple
#stocks.columns=stocks.columns.to_flat_index()

close = stocks.loc[:, "Close"].copy()

normal_close = close.div(close.iloc[0]).mul(100)

normal_close.plot(figsize=(15,8), fontsize=12)
plt.legend(fontsize=12)
plt.show()