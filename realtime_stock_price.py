import requests

def get_realtime_stock_price(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    try:
        price = data['Global Quote']['05. price']
        return float(price)
    except (KeyError, ValueError):
        print("Error fetching price. Check symbol and API key.")
        return None

if __name__ == "__main__":
    # Replace with your Alpha Vantage API key
    API_KEY = "47JMAJC6GA0I00VX"

"
    # Example stock symbol
    SYMBOL = "AAPL"
    price = get_realtime_stock_price(SYMBOL, API_KEY)
    if price:
        print(f"Real-time price for {SYMBOL}: ${price}")
    else:
        print("Failed to fetch real-time price.")
