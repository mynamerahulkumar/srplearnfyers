

import pandas as pd
from fyers_apiv3 import fyersModel
import datetime as dt
import pytz

#generate trading session
client_id = open("secrets/client_id.txt",'r').read()
access_token = open("secrets/access_token.txt",'r').read()

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="/Users/rahulkumar/Documents/GitHub/srplearnfyers/1fyersalgotrade/logs")


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
    response = fyers.history(data=data)
    print("response----",response)
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
response_df = fetchOHLC2("NSE:RELIANCE-EQ","5",5)
# 5 min dataframe,last 5 days

# Print the DataFrame
print(response_df)

# Save data to a CSV file
response_df.to_csv('output_data/output_duration.csv', index=False)



