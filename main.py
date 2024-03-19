import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ticker = ["SPY", "AAPL", "KO", "IBM", "DIS", "MSFT"]

stocks = yf.download(ticker, start = "2010-01-01", end = "2021-01-01")

stocks.to_csv("stocksYT.csv")

stocks = pd.read_csv("stocksYT.csv", header = [0,1], index_col=[0], parse_dates=[0])

# convert multi index to tuple
#stocks.columns=stocks.columns.to_flat_index()

close = stocks.loc[:, "Close"].copy()

normal_close = close.div(close.iloc[0]).mul(100)

#normal_close.plot(figsize=(15,8), fontsize=12)
#plt.legend(fontsize=12)
#plt.show()

aapl = close.AAPL.copy().to_frame()
#aapl["lag1"]=aapl.shift(periods=1)
#aapl["Diff"]=aapl.AAPL.sub(aapl.lag1)
#aapl["Daily Change"]=aapl.AAPL.div(aapl.lag1).sub(1).mul(100)
#aapl["% Change 2"]=aapl.AAPL.pct_change(periods=1).mul(100)

##calculate monthly business day percent change
# aapl.AAPL.resample("BME").last().pct_change(periods=1).mul(100)

ret = close.pct_change().dropna()

# show a histogram of aapl returns
#ret.plot(kind="hist", figsize=(12,8), bins=100)
#plt.show()

daily_mean_return = ret.mean()
var_daily = ret.var()
std_daily = np.sqrt(var_daily)
#alternate standard dev calc
# ret.std()

annual_mean_ret = daily_mean_return*252
annual_var_ret = var_daily*252
annual_std_ret = np.sqrt(annual_var_ret)

#alt annual std calc
# ret.std().np.sqrt(252)

#Transpose the outout of .describe()
# ret.describe().T

#add loc func to above
summary = ret.describe().T.loc[:, ["mean", "std"]]

summary["mean"]=summary["mean"]*252
summary["std"]=summary["std"]*np.sqrt(252)