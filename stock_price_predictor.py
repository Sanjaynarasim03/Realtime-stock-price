import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta

# Fetch historical daily prices from Alpha Vantage

def fetch_historical_data(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'Time Series (Daily)' not in data:
        print(f"No data found for symbol '{symbol}'. Please check if the symbol is correct and supported by Alpha Vantage.")
        print("Try a supported symbol like 'AAPL', 'MSFT', 'TSLA', 'GOOGL', 'INFY', etc.")
        return None
    try:
        ts = data['Time Series (Daily)']
        df = pd.DataFrame.from_dict(ts, orient='index')
        df = df.rename(columns={'4. close': 'close'})
        df['close'] = df['close'].astype(float)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        return df[['close']]
    except Exception as e:
        print("Error processing historical data:", e)
        return None

# Train and predict next 7 days

def predict_next_week(df):
    df = df.reset_index()
    df['day_num'] = (df['index'] - df['index'].min()).dt.days
    X = df[['day_num']]
    y = df['close']
    model = LinearRegression()
    model.fit(X, y)
    last_day = df['day_num'].iloc[-1]
    future_days = np.array([last_day + i for i in range(1, 8)]).reshape(-1, 1)
    preds = model.predict(future_days)
    future_dates = [df['index'].iloc[-1] + timedelta(days=i) for i in range(1, 8)]
    return list(zip(future_dates, preds))

if __name__ == "__main__":
    API_KEY = "47JMAJC6GA0I00VX"  # Replace with your Alpha Vantage API key
    SYMBOL = "AAPL"  # Example stock symbol
    df = fetch_historical_data(SYMBOL, API_KEY)
    if df is not None:
        predictions = predict_next_week(df)
        print(f"Predicted closing prices for {SYMBOL} for the next 7 days:")
        for date, price in predictions:
            print(f"{date.date()}: ${price:.2f}")
    else:
        print("Prediction aborted due to missing or invalid data.")
