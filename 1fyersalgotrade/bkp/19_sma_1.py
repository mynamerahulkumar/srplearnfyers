# -*- coding: utf-8 -*-
"""
Created By: Aseem Singhal

"""
import pandas as pd

file_name = "sbin_1min.csv"
data = pd.read_csv(file_name, parse_dates=['Date'])
data = data.sort_values('Date')
print(data)

#SMA-1
sma = data['Close'].rolling(window=14).mean()
data['SMA'] = sma
#data.to_csv("sma_1.csv", index=False)
print(data)


