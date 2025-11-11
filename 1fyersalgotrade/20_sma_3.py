
import pandas as pd

file_name = "sbin_1min.csv"
data = pd.read_csv(file_name, parse_dates=['Date'])
data = data.sort_values('Date')
#print(data)

#SMA - 3
sma_list = []
period = 14
sma_value = 0
for i in range (len(data)):
    if i >= period - 1:
        sma_value = 0
        for j in range (0, period):
            sma_value = sma_value + data.loc[i-j,'Close']
        sma_value = sma_value / period
        sma_list.append(sma_value)
    else:
        sma_list.append(None)

data['SMA'] = sma_list
print(data)


