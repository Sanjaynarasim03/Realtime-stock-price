from flask import Flask, render_template_string, request
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Stock Price Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        input, button { padding: 8px; margin: 4px; }
        table { border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; }
    </style>
</head>
<body>
    <h2>Stock Price Predictor</h2>
    <form method="post">
        <label>Stock Symbol:</label>
        <input name="symbol" value="AAPL" required>
        <button type="submit">Predict</button>
    </form>
    {% if predictions %}
    <h3>Predicted closing prices for {{ symbol }} for the next 7 days:</h3>
    <table>
        <tr><th>Date</th><th>Predicted Price ($)</th></tr>
        {% for date, price in predictions %}
        <tr><td>{{ date }}</td><td>{{ price }}</td></tr>
        {% endfor %}
    </table>
    {% elif error %}
    <p style="color:red;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

API_KEY = "47JMAJC6GA0I00VX"  # Replace with your Alpha Vantage API key

def fetch_historical_data(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'Time Series (Daily)' not in data:
        return None, f"No data found for symbol '{symbol}'. Try AAPL, MSFT, TSLA, GOOGL, INFY, etc."
    try:
        ts = data['Time Series (Daily)']
        df = pd.DataFrame.from_dict(ts, orient='index')
        df = df.rename(columns={'4. close': 'close'})
        df['close'] = df['close'].astype(float)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        return df[['close']], None
    except Exception as e:
        return None, f"Error processing historical data: {e}"

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
    return [(d.date(), f"{p:.2f}") for d, p in zip(future_dates, preds)]

@app.route('/', methods=['GET', 'POST'])
def index():
    predictions = None
    error = None
    symbol = 'AAPL'
    if request.method == 'POST':
        symbol = request.form['symbol'].upper()
        df, error = fetch_historical_data(symbol, API_KEY)
        if df is not None:
            predictions = predict_next_week(df)
    return render_template_string(HTML, predictions=predictions, error=error, symbol=symbol)

if __name__ == '__main__':
    app.run(debug=True)
