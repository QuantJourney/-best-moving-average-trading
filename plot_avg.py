import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

stockData = yf.Ticker("MCD")

# Get stock info
data = stockData.history(period="5y")

# Get close price
close = data['Close'].to_numpy()

# Avg calc
def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

# Avg
shortAvg = 10
longAvg = 50

shortAvgX = np.arange(shortAvg - 1, len(close))
shortAvgY = moving_average(close, shortAvg)

longAvgX = np.arange(longAvg - 1, len(close))
longAvgY = moving_average(close, longAvg)

plt.plot(close)
plt.plot(shortAvgX, shortAvgY)
plt.plot(longAvgX, longAvgY)
plt.show()
