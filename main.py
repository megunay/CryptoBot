import ccxt
import time
import pandas as pd

# Binance API Keys (use test keys if available)
API_KEY = "l2FduDgvwXVbtPaulJ5SSesoBZvqTlydnGcsZ9jVO6Bh1ssBuWSykCIgdclVE3DD"
API_SECRET = "979k6kjZ7NT3i0uv1M4eboV3L7yX8OZ9Of5O8FjkmcEQxGDnuykNzmMSkkDkubor"

# Initialize Binance exchange
exchange = ccxt.binance({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "options": {"defaultType": "spot"},
    "rateLimit": 1200,
})

exchange.set_sandbox_mode(True)

# Fetch historical data
def get_historical_data(symbol="BTC/USDT", timeframe="1m", limit=50):
    bars = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

# Simple Moving Average Strategy
def moving_average_strategy(symbol="BTC/USDT"):
    df = get_historical_data(symbol)
    df["SMA_5"] = df["close"].rolling(5).mean()
    df["SMA_10"] = df["close"].rolling(10).mean()
    
    # Trading condition
    if df["SMA_5"].iloc[-1] > df["SMA_10"].iloc[-1]:
        print("Buy Signal! Placing order...")
        return "buy"
    elif df["SMA_5"].iloc[-1] < df["SMA_10"].iloc[-1]:
        print("Sell Signal! Placing order...")
        return "sell"
    else:
        return "hold"

# Place a test order
def place_order(symbol, side, amount=0.001):
    order = exchange.create_market_order(symbol, side, amount)
    print("Order placed:", order)

# Main loop
def run_bot():
    while True:
        try:
            decision = moving_average_strategy("BTC/USDT")
            print("Decision:", decision)
            
            if decision == "buy":
                place_order("BTC/USDT", "buy")
            elif decision == "sell":
                place_order("BTC/USDT", "sell")

            time.sleep(60)
        except Exception as e:
            print("Error in bot loop:", e)
            time.sleep(10)  # Prevent infinite crashing


run_bot()