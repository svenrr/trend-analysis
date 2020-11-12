import streamlit as st
import pandas as pd 
from pytrends.request import TrendReq
import time
import datetime

#from news_scraping import get_urls_from_feed
#
#st.write("# BBC News Scraper")
#
#if st.button("Fetch..."): 
#  get_urls_from_feed()


pytrends = TrendReq(hl='en-US', tz=360)
keywords = ["Joe Biden", "Donald Trump"]
pytrends.build_payload(keywords, timeframe="today 5-y", geo="US")
df = pytrends.interest_over_time()

st.write("# Keyword Search")

st.dataframe(df)

df1 = pytrend.trending_searches(pn='germany')

st.write("# Trending Search")
st.dataframe(df1)
