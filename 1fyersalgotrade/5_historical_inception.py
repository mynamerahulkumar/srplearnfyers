

import os
import datetime as dt
import pandas as pd
from fyers_apiv3 import fyersModel
import pytz


#generate trading session
client_id = open("secrets/client_id.txt",'r').read()
access_token = open("secrets/access_token.txt",'r').read()

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="/Users/rahulkumar/Documents/GitHub/srplearnfyers/1fyersalgotrade/logs")


def fetchOHLC_full(ticker,interval,inception_date):

    from_date = dt.datetime.strptime(inception_date, '%Y-%m-%d')
    to_date = dt.date.today()

    # Create a DataFrame
    columns = ['Timestamp','Open','High','Low','Close','Volume']
    df = pd.DataFrame(columns=columns)
## get all data by 50 days loop if there is more data
    while True:
        from_date_string = from_date.strftime("%Y-%m-%d") #2025-05-01 +50 day (2025-06-21)# #next from.(2025-06-22)
        ttoday = dt.date.today()
        to_date_string = ttoday.strftime("%Y-%m-%d")#2025-10-30 #(2025-10-01)

        if from_date.date() >= (dt.date.today() - dt.timedelta(50)):
            data = {
                "symbol":ticker,
                "resolution":interval,
                "date_format":"1",
                "range_from":from_date_string,
                "range_to":to_date_string,
                "cont_flag":"1"
            }
            resp = fyers.history(data=data)['candles']
            df1 = pd.DataFrame(resp, columns=columns)
            result = pd.concat([df, df1], ignore_index=True)
            df = result
            break
        else:
            to_date = from_date + dt.timedelta(50)
            to_date_string = to_date.strftime("%Y-%m-%d")
            data = {
                "symbol":ticker,
                "resolution":interval,
                "date_format":"1",
                "range_from":from_date_string,
                "range_to":to_date_string,
                "cont_flag":"1"
            }
            resp = fyers.history(data=data)['candles']
            df1 = pd.DataFrame(resp, columns=columns)
            result = pd.concat([df, df1], ignore_index=True)
            df = result
            from_date = to_date + dt.timedelta(1)

    # Convert Timestamp to datetime in UTC
    df['Timestamp2'] = pd.to_datetime(df['Timestamp'],unit='s').dt.tz_localize(pytz.utc)

    # Convert Timestamp to IST
    ist = pytz.timezone('Asia/Kolkata')
    df['Timestamp2'] = df['Timestamp2'].dt.tz_convert(ist)

    return (df)

# Fetch OHLC data using the function
response_df = fetchOHLC_full("NSE:NIFTY50-INDEX","5","2025-05-01")

# Print the DataFrame
print(response_df)

# Save data to a CSV file
response_df.to_csv('output_data/output_full.csv', index=False)


