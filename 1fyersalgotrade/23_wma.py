
import pandas as pd

file_name = "sbin_1min.csv"
data = pd.read_csv(file_name, parse_dates=['Date'])
data = data.sort_values('Date')
#print(data)

#WMA 10% , 20% , 30% , 40%
wma_list = []
period = 4
wma_value = 0
wma_perc = [0.40,0.30,0.20,0.10]
for i in range (len(data)):
    if i >= period - 1:
        wma_value = 0
        for j in range (0, period):
            wma_value = wma_value + (data.loc[i-j,'Close'])*wma_perc[j]
        wma_list.append(wma_value)

    else:
        wma_list.append(None)


data['WMA'] = wma_list
print(data)
