# -*- coding: utf-8 -*-
"""
Created By: Aseem Singhal

"""
import pandas as pd
import numpy as np

file_name = "sbin_1min.csv"
data = pd.read_csv(file_name, parse_dates=['Date'])
data = data.sort_values('Date')
#print(data)

#ATR
window = 14  # You can adjust the window size for ATR calculation
atr = []
for i in range(len(data)):
    if i >= window:
        tr_values = []
        for j in range(window):
            high = data.iloc[i - j]['High']
            low = data.iloc[i - j]['Low']
            close_prev = data.iloc[i - j - 1]['Close']
            tr = max(high - low, abs(high - close_prev), abs(low - close_prev))
            tr_values.append(tr)
        atr.append(sum(tr_values) / window)

    else:
        atr.append(None)

data['ATR'] = atr
print(data)
