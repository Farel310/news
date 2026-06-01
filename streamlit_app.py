import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Terminal Trading", layout="wide")
st.title("📈 TERMINAL TRADING LEVEL 1")

# TICKER GOLD DIGANTI JADI GC=F
pairs = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD", 
    "Gold": "GC=F",  # <- INI YANG DIBENERIN. DULU XAUUSD=X
    "EUR/USD": "EURUSD=X",
    "USD/JPY": "USDJPY=X",
    "DXY": "DX-Y.NYB"
}

col1, col2 = st.columns([1,3])

with col1:
    pair_label = st.selectbox("Pilih Pair:", list(pairs.keys()))
    pair = pairs[pair_label]

    timeframe = st.selectbox("Timeframe:", ["1h", "1d", "1wk"])
    period = st.selectbox("Period:", ["5d", "1mo", "3mo", "1y"])

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
        st.error("⚠️ Data kosong. Coba refresh atau ganti pair")

st.caption(f"Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
