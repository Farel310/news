import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Terminal Trading", layout="wide")
st.title("📈 TERMINAL TRADING LEVEL 1")

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
    pair_label = st.selectbox("Pilih Pair:", list(pairs.values()))
    pair = list(pairs.keys())[list(pairs.values()).index(pair_label)]

    timeframe = st.selectbox("Timeframe:", ["1m", "5m", "15m", "1h", "1d"])
    period = st.selectbox("Period:", ["1d", "5d", "1mo", "3mo", "6mo", "1y"])

df = yf.download(pair, period=period, interval=timeframe)

with col1:
    if not df.empty:
        price = float(df['Close'].iloc[-1])
        st.metric(pair_label, f"${price:,.2f}")
    else:
        st.metric(pair_label, "Data Kosong")

with col2:
    if not df.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close']
        )])
        fig.update_layout(
            title=f"Grafik {pair_label} - {timeframe}",
            xaxis_title="Waktu", yaxis_title="Harga USD",
            xaxis_rangeslider_visible=False, height=600
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Data ga ada. Coba period 1mo + timeframe 1h")

st.caption(f"Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
