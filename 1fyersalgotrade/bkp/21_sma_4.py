# -*- coding: utf-8 -*-
"""
Created By: Aseem Singhal

"""
import pandas as pd

file_name = "sbin_1min.csv"
data = pd.read_csv(file_name, parse_dates=['Date'])
data = data.sort_values('Date')
#print(data)

#SMA - 4
sma_list = []
close_value = []
period = 14
sma_value = 0
for index, row in data.iterrows():
    close_value.append(row['Close'])
    if index >= period - 1:
        sma_value = 0
        for i in range (0, period):
            sma_value = sma_value + close_value[index-i]
        sma_value = sma_value / period
        sma_list.append(sma_value)
    else:
        sma_list.append(None)

data['SMA'] = sma_list
print(data)




