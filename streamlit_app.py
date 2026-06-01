import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Terminal Trading", layout="wide")
st.title("📈 TERMINAL TRADING LEVEL 1")

# List pair
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
    pair_label = st.selectbox("Pilih Pair:", list(pairs.keys()), format_func=lambda x: pairs[x])
    pair = pair_label

    timeframe = st.selectbox("Timeframe:", ["1m", "5m", "15m", "1h", "1d"])
    period = st.selectbox("Period:", ["1d", "5d", "1mo", "3mo", "6mo", "1y"])

# Ambil data dulu
df = yf.download(pair, period=period, interval=timeframe)

with col1:
    if not df.empty:
        # Ambil harga terakhir dari df
        price = float(df['Close'].iloc[-1])
        st.metric(pair_label, f"${price:,.2f}") # <- UDAH DIGANTI pair_label
    else:
        st.metric(pair_label, "Data Kosong") # <- UDAH DIGANTI pair_label

# Grafik candlestick
with col2:
    if not df.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close']
        )])
        fig.update_layout(
            title=f"Grafik {pairs[pair]} - {timeframe}", # <- ini juga gua benerin
            xaxis_title="Waktu",
            yaxis_title="Harga USD",
            xaxis_rangeslider_visible=False,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Data ga ada. Coba ganti timeframe jadi 1h/1d atau period jadi 1mo")

st.caption(f"Update terakhir: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
