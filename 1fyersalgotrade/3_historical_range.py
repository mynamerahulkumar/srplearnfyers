

import pandas as pd
from fyers_apiv3 import fyersModel
import pytz


#generate trading session
client_id = open("secrets/client_id.txt",'r').read()
access_token = open("secrets/access_token.txt",'r').read()

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="/Users/rahulkumar/Documents/GitHub/srplearnfyers/1fyersalgotrade/logs")

def fetchOHLC(ticker,interval,range_from, range_to):
    data = {
        "symbol":ticker,
        "resolution":interval,
        "date_format":"1",
        "range_from":range_from,
        "range_to":range_to,
        "cont_flag":"1"
    }

    '''
    1 minute : “1”
    2 minute : “2"
    3 minute : "3"
    5 minute : "5"
    10 minute : "10"
    15 minute : "15"
    20 minute : "20"
    30 minute : "30"
    60 minute : "60"
    120 minute : "120"
    240 minute : "240"
    Daily : "D"
    range format: yyyy-mm-dd
    '''
    # response = fyers.history(data=data)
    # print(response)
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

# Fetch OHLC data using the function
response_df = fetchOHLC("NSE:HDFCBANK-EQ","5","2025-08-18", "2025-10-25")# yyyy-mm-dd

# Print the DataFrame
print(response_df)

# Save data to a CSV file
response_df.to_csv('output_data/output_eq.csv', index=False)



