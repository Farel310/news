import streamlit as st
import feedparser
from datetime import datetime
import time

st.set_page_config(page_title="Berita Realtime Trader", layout="wide", page_icon="🚨")
st.title("🚨 DASHBOARD BERITA REALTIME TRADER")

RSS_FEEDS = {
    "Reuters": "http://feeds.reuters.com/reuters/topNews",
    "Bloomberg": "https://feeds.bloomberg.com/markets/news.rss", 
    "ForexLive": "https://www.forexlive.com/feed/",
    "Kitco Gold": "https://www.kitco.com/rss/kitconews.xml"
}

refresh = st.slider("Refresh tiap detik:", 10, 120, 30)
keyword = st.text_input("Filter keyword:",)

if 'last_titles' not in st.session_state:
    st.session_state.last_titles = set()

all_news = []
for source, url in RSS_FEEDS.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:10]:
        all_news.append({'title': entry.title, 'link': entry.link, 'source': source, 'time': entry.get('published', 'N/A')})

keywords = [k.strip().lower() for k in keyword.split(',')]
filtered = [n for n in all_news if any(k in n['title'].lower() for k in keywords)]

new_titles = set([n['title'] for n in filtered])
new_count = len(new_titles - st.session_state.last_titles)
if new_count > 0:
    st.error(f"🚨 BREAKING! {new_count} BERITA BARU MASUK!")
    st.balloons()
st.session_state.last_titles = new_titles

st.write(f"**{len(filtered)} berita terbaru**")
for news in filtered[:20]:
    with st.container(border=True):
        st.subheader(news['title'])
        st.caption(f"{news['source']} | {news['time']}")
        st.link_button("Buka Berita", news['link'])
time.sleep(refresh)
st.rerun()
