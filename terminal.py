import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Terminal Trading Level 1", layout="wide")
st.title("📊 TERMINAL TRADING LEVEL 1")

# Sidebar pair
pairs = {
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum",
    "XAUUSD=X": "Gold",
    "EURUSD=X": "EUR/USD",
    "USDJPY=X": "USD/JPY",
    "DX-Y.NYB": "DXY Dollar Index"
}

col1, col2 = st.columns([1,3])

with col1:
    pair = st.selectbox("Pilih Pair:", list(pairs.keys()), format_func=lambda x: pairs[x])
    timeframe = st.selectbox("Timeframe:", ["1m", "5m", "15m", "1h", "4h", "1d"], index=2)
    period = st.selectbox("Period:", ["1d", "5d", "1mo", "3mo"], index=2)

    # Harga real-time
    ticker = yf.Ticker(pair)
    data = ticker.history(period="1d", interval="1m")
    if not data.empty:
        price = data['Close'][-1]
        change = price - data['Open'][-1]
        change_pct = (change/data['Open'][-1])*100
        st.metric(pairs[pair], f"${price:,.2f}", f"{change_pct:.2f}%")

with col2:
    # Chart candlestick
    df = yf.download(pair, period=period, interval=timeframe)
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close']
    )])
    fig.update_layout(height=500, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption(f"Update: {datetime.now().strftime('%H:%M:%S')} WIB | Data dari Yahoo Finance")
st.caption("Refresh manual pake tombol R di keyboard")
