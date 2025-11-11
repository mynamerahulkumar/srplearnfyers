"""
Created By: Aseem Singhal
Fyers API V3

"""
import datetime as dt
from fyers_apiv3 import fyersModel
import pandas as pd
import pytz
import matplotlib.pyplot as plt
import mplfinance as mpf

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
    df.drop(columns=['Timestamp'], inplace=True)

    return (df)


def bollingerBand(DF,window=15, num_std_devs=2):
    "function to calculate Bollinger Band"
    df = DF.copy()
    df["MA"] = df['Close'].rolling(window).mean()
    df["BB_up"] = df["MA"] + df['Close'].rolling(window).std()*num_std_devs
    df["BB_dn"] = df["MA"] - df['Close'].rolling(window).std()*num_std_devs
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    df.dropna(inplace=True)
    return df


# Fetch OHLC data using the function
stock_df = fetchOHLC2("NSE:SBIN-EQ","30",5)
print(stock_df)

bb_df = bollingerBand(stock_df,15)
print(bb_df)

df = pd.DataFrame(bb_df)
df['Timestamp2'] = pd.to_datetime(df['Timestamp2'])
df.set_index('Timestamp2', inplace=True)
print(df)

# Create a plot with a candlestick chart and Bollinger Bands as lines
mpf.plot(df, type='candle', style='charles', title='Candlestick Chart with Bollinger Bands',
         addplot=[
             mpf.make_addplot(df['BB_up'], panel=0, color='orange', secondary_y=False),
             mpf.make_addplot(df['BB_dn'], panel=0, color='cyan', secondary_y=False),
             mpf.make_addplot(df['MA'], panel=0, color='black', secondary_y=False)
         ])
