# -*- coding: utf-8 -*-
"""
Created By: Aseem Singhal

"""
import pandas as pd

file_name = "sbin_1min.csv"
data = pd.read_csv(file_name, parse_dates=['Date'])
data = data.sort_values('Date')
#print(data)

#EMA
ema = data['Close'].ewm(span=14).mean()
data['EMA'] = ema
#data.to_csv("ema_1.csv", index=False)
print(data)


