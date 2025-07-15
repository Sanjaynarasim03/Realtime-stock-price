# Realtime-stock-price

## Overview
This project provides a Python script to fetch real-time and historical stock prices using the Alpha Vantage API, and predicts the next 7 days' closing prices using a simple machine learning model (Linear Regression).

## Features
- Fetch real-time and historical stock prices for supported symbols (AAPL, MSFT, TSLA, GOOGL, INFY, etc.)
- Predict closing prices for the next week using ML

## Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/Sanjaynarasim03/Realtime-stock-price.git
   cd Realtime-stock-price
   ```
2. Install dependencies:
   ```sh
   python3 -m pip install requests pandas scikit-learn numpy
   ```
3. Get a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key) and update the `API_KEY` variable in `stock_price_predictor.py`.

## Usage
Run the predictor script:
```sh
python3 stock_price_predictor.py
```
You can change the stock symbol by editing the `SYMBOL` variable in the script.

## Example Output
```
Predicted closing prices for AAPL for the next 7 days:
2025-07-15: $194.43
2025-07-16: $194.22
...
```

## Notes
- Only supported symbols will work. If you get a 'No data found' error, try a different symbol.
- For more advanced ML models or visualizations, contributions are welcome!
