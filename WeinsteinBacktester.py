import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class WeinsteinBacktester():
    def __init__(self, symbol, start, end):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.results = None
        self.get_data()

    def get_data(self):
        df = yf.download(self.symbol, start=self.start, end=self.end)
        data = df.Close.to_frame()
        data["returns"] = np.log(data.Close.div(data.Close.shift(1)))
        data["30W"] = data.Close.rolling(window=(7*30)).mean()
        data.dropna(inplace=True)
        self.data_two = data

        return data
    
    def test_results(self):
        data=self.data_two.copy().dropna()
        data["position"] = np.where(data["Close"] > data["30W"], 1, 0)
        data["strategy"] = data["returns"] * data.position.shift(1)
        data.dropna(inplace=True)
        data["returns_bh"] = data["returns"].cumsum().apply(np.exp)
        data["returns_strategy"] = data["strategy"].cumsum().apply(np.exp)
        perf = data["returns_strategy"].iloc[-1]
        outperf = perf - data["returns_bh"].iloc[-1]
        self.results=data

        ret = round(np.exp(data["strategy"].sum()), 2)
        std = round(data["strategy"].std() * np.sqrt(252), 2)

        return round(perf, 6), round(outperf, 6)
    
    def plot_results(self):
        if self.results is None:
            print("Run the test please")
        else:
            title=f"{self.symbol}| 30W Crossover"
            self.results[["returns_bh", "returns_strategy"]].plot(title=title, figsize=(12,8))