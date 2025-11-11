# -*- coding: utf-8 -*-
"""
Created By: Aseem Singhal
Fyers API V3

"""
import datetime as dt
from fyers_apiv3 import fyersModel
import pandas as pd
import pytz
import matplotlib.pyplot as plt

#generate trading session
client_id = open("client_id.txt",'r').read()
access_token = open("access_token.txt",'r').read()

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

def fetchOHLC2(ticker,interval,duration):
    range_from = dt.date.today()-dt.timedelta(duration)
    range_to = dt.date.today()

    from_date_string = range_from.strftime("%Y-%m-%d")
    to_date_string = range_to.strftime("%Y-%m-%d")
    data = {
        "symbol":ticker,
        "resolution":interval,
        "date_format":"1",
        "range_from":from_date_string,
        "range_to":to_date_string,
        "cont_flag":"1"
    }

    response = fyers.history(data=data)['candles']

    # Create a DataFrame
    columns = ['Timestamp','Open','High','Low','Close','Volume']
    df = pd.DataFrame(response, columns=columns)

    # Convert Timestamp to datetime in UTC
    df['Timestamp2'] = pd.to_datetime(df['Timestamp'],unit='s').dt.tz_localize(pytz.utc)

    # Convert Timestamp to IST
    ist = pytz.timezone('Asia/Kolkata')
    df['Timestamp2'] = df['Timestamp2'].dt.tz_convert(ist)

    return (df)


def MACD(DF,a,b,c):
    """function to calculate MACD
       typical values a(fast moving average) = 12; 
                      b(slow moving average) =26; 
                      c(signal line ma window) =9"""
    df = DF.copy()
    df["MA_Fast"]=df["Close"].ewm(span=a,min_periods=a).mean()
    df["MA_Slow"]=df["Close"].ewm(span=b,min_periods=b).mean()
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
    df["Signal"]=df["MACD"].ewm(span=c,min_periods=c).mean()
    df.dropna(inplace=True)
    return df


# Fetch OHLC data using the function
stock_df = fetchOHLC2("NSE:SBIN-EQ","30",100)
print(stock_df)

macd_df = MACD(stock_df,12,26,9)
print(macd_df)


# Create a plot with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot the CLOSE price of the stock
ax1.plot(stock_df.index, stock_df['Close'], label='Close Price', color='blue')
ax1.set_ylabel('Close Price')
ax1.legend()

# Plot the MACD and Signal line
ax2.plot(macd_df.index, macd_df['MACD'], label='MACD', color='orange')
ax2.plot(macd_df.index, macd_df['Signal'], label='Signal Line', color='green')
ax2.set_xlabel('Date')
ax2.set_ylabel('MACD')
ax2.legend()

plt.tight_layout()
plt.show()
