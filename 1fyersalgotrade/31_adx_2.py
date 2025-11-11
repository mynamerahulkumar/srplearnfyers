# -*- coding: utf-8 -*-
"""
Created By: Aseem Singhal

"""
import pandas as pd

file_name = "sbin_1min.csv"
data = pd.read_csv(file_name, parse_dates=['Date'])
data = data.sort_values('Date')
#print(data)


#ADX
'''
Calculate the True Range (TR). True range is the Max of:
Current High minus Current Low
Current High minus Previous Close
Current Low minus Previous Close
Calculate the directional movement +DM1 and -DM1. Directional movement is positive  when the current high minus the previous high is greater than the previous low minus the current low. This so-called Plus Directional Movement (+DM) then equals the current high minus the prior high, provided it is positive. A negative value would simply be entered as zero. Directional movement is negative (minus) when the previous low minus the current low is greater than the current high minus the previous high. This so-called Minus Directional Movement (-DM) equals the prior low minus the current low, provided it is positive. A negative value would simply be entered as zero.
Calculate 14 period moving average of True range (TR14). Here the period 14 corresponds to the ADX period 14.
Calculate 14 period moving average of +DM1 and -DM1. It would be called +DM14 and -DM14.
Calculate +DI14 and -DI14.
+DI14 is the ratio of +DM14 and TR14 expressed in % terms.
-DI14 is the ratio of -DM14 and TR14 expressed in % terms.
Calculate Directional Movement Index (DX). It equals the absolute value of +DI14 minus -DI14 divided by the sum of +DI14 and – DI14. It is also expressed in % terms.
Calculate Average directional index (ADX). It is the 14 period moving average of DX.
'''

period = 14
dmplus = []
dmminus = []
dmplus14 = []
dmminus14 = []
diplus14 = []
diminus14 = []
dx = []
adx = []

#ATR------------------------
data['High-Low']=abs(data['High']-data['Low'])
data['High-PrevClose']=abs(data['High']-data['Close'].shift(1))
data['Low-PrevClose']=abs(data['Low']-data['Close'].shift(1))
data['TR']=data[['High-Low','High-PrevClose','Low-PrevClose']].max(axis=1,skipna=False)
data['ATR'] = data['TR'].ewm(com=period,min_periods=period).mean()
#-----------------------------


for i in range (len(data)):
    if i >= period:
        if (data.loc[i,'High'] - data.loc[i-1,"High"]) > (data.loc[i-1,"Low"] - data.loc[i,"Low"]):
            dmplus.append(data.loc[i,'High'] - data.loc[i-1,"High"])
            dmminus.append(0)
        else:
            dmplus.append(0)
            dmminus.append(data.loc[i-1,"Low"] - data.loc[i,"Low"])

    else:
        dmminus.append(0)
        dmplus.append(0)

data['dmplus'] = dmplus
data['dmminus'] = dmminus

for i in range (len(data)):
    if i >= period:
        var1 = 0
        var2 = 0
        for j in range (period):
            var1 = var1 + data.loc[i-j,'dmplus']
            var2 = var2 + data.loc[i-j,'dmminus']

        var1 = var1/period
        var2 = var2/period
        dmplus14.append(var1)
        dmminus14.append(var2)
    else:
        dmplus14.append(0)
        dmminus14.append(0)

data['dmplus14'] = dmplus14
data['dmminus14'] = dmminus14


for i in range (len(data)):
    if i >= period:
        diplus14.append(data.loc[i,'dmplus14']*100 / data.loc[i,'ATR'])
        diminus14.append(data.loc[i,'dmminus14']*100 / data.loc[i,'ATR'])
    else:
        diplus14.append(0)
        diminus14.append(0)

#Calculate Directional Movement Index (DX).
# It equals the absolute value of +DI14 minus -DI14 divided by the sum of +DI14 and – DI14.
# It is also expressed in % terms


data['diplus14'] = diplus14
data['diminus14'] = diminus14


for i in range(len(data)):
    if i >= period:
        dx.append(abs(data.loc[i,'diplus14'] - data.loc[i,'diminus14']) * 100 / (data.loc[i,'diplus14'] + data.loc[i,'diminus14']) )
    else:
        dx.append(0)

data['dx'] = dx


for i in range (len(data)):
    if i >= period+(period - 1):
        var1 = 0
        for j in range (period):
            var1 = var1 + data.loc[i-j,'dx']

        var1 = var1/period
        adx.append(var1)
    else:
        adx.append(0)

data['adx'] = adx
print(data)

