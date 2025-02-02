import streamlit as st
import ccxt
import pandas as pd
import time

# Binance API Keys
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

# Initialize Binance exchange
exchange = ccxt.binance({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "options": {"defaultType": "spot"},
    "rateLimit": 1200,
})
exchange.set_sandbox_mode(True)  # Enable test mode

# Fetch historical data
def get_historical_data(symbol="BTC/USDT", timeframe="1m", limit=50):
    bars = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

# UI Layout
st.title("Crypto Trading Bot")
st.sidebar.header("Settings")
symbol = st.sidebar.selectbox("Select Trading Pair", ["BTC/USDT", "ETH/USDT"])
timeframe = st.sidebar.selectbox("Select Timeframe", ["1m", "5m", "15m", "1h"])
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 5, 60, 10)

# Fetch and display data
st.subheader(f"{symbol} Market Data")
df = get_historical_data(symbol, timeframe)
st.line_chart(df.set_index("timestamp")["close"])

# Trading decision logic
def moving_average_strategy(df):
    df["SMA_5"] = df["close"].rolling(5, min_periods=1).mean()
    df["SMA_10"] = df["close"].rolling(10, min_periods=1).mean()

    if df["SMA_5"].iloc[-1] > df["SMA_10"].iloc[-1]:
        return "Buy Signal"
    elif df["SMA_5"].iloc[-1] < df["SMA_10"].iloc[-1]:
        return "Sell Signal"
    else:
        return "Hold"

decision = moving_average_strategy(df)
st.subheader(f"Trading Decision: {decision}")

# Auto-refreshing
time.sleep(refresh_rate)
st.rerun()