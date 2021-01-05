import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

stockData = yf.Ticker("MCD")

# Get stock info
data = stockData.history(period="5y")

# Get close price
close = data['Close'].to_numpy()
length = len(close)

# Take portion for train
train = close[0:int(length * 0.7)]
test = close[int(length * 0.7):length]

# Avg calc
def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

# Sweep
shortAvgValues = np.arange(5, 30)
longAvgValues = np.arange(40, 300)

bestProfits = -99999999
bestShort = 0
bestLong = 0

def calc_profits(data, s, l):

    shortAvgX = np.arange(s - 1, len(data))
    shortAvgY = moving_average(data, s)

    longAvgX = np.arange(l - 1, len(data))
    longAvgY = moving_average(data, l)

    shortAvgX = shortAvgX[l-s:]
    shortAvgY = shortAvgY[l-s:]

    # Find buy/sell points
    diff = longAvgY - shortAvgY
    buys = []
    sells = []

    for d in np.arange(len(diff)):
        if (diff[d] >= 0 and diff[d-1] <= 0):
            sells.append(d + l)
        if (diff[d] <= 0 and diff[d-1] >= 0):
            buys.append(d + l)

    if (len(buys) > len(sells)):
        buys.pop()

    try:

        fees = 0
        buy_fees = np.sum(data[buys] * fees)
        sell_fees = np.sum(data[sells] * fees)
        total_fees = buy_fees + sell_fees

        total = np.sum(data[sells] - data[buys]) - total_fees
        return total
    except:
        return -999999


for s in shortAvgValues:
    for l in longAvgValues:

        profit_train = calc_profits(train, s, l) / len(train)
        profit_test = calc_profits(test, s, l) / len(test)

        total = profit_test + profit_train

        if ((profit_test > 0) and (profit_train > 0)):
            if (total > bestProfits):
                bestProfits = total
                bestShort = s
                bestLong = l
                print('Train profit / unit:', profit_train)
                print('Test profit / unit:', profit_test)


print('Profits:', bestProfits)
print('Best short average:', bestShort)
print('Best long average:', bestLong)
